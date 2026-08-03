"""Calculate financial analysis metrics from Apple's source financial data.

The raw CSV remains unchanged. This module adds derived metrics that are useful
for dashboard analysis, SQL queries, and Excel reporting.
"""

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from scripts.load_financial_data import load_apple_financials

PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "apple_financial_metrics_2022_2025.csv"
PERCENTAGE_COLUMNS = [
    "revenue_growth_rate",
    "net_income_growth_rate",
    "gross_margin",
    "operating_margin",
    "net_profit_margin",
    "free_cash_flow_margin",
    "return_on_equity",
]


def add_calculated_metrics(financials: pd.DataFrame) -> pd.DataFrame:
    """Add common financial analysis metrics to Apple's annual data.

    ROE uses ending shareholders' equity, per the MVP decision.
    """
    metrics = financials.sort_values("fiscal_year").copy()

    metrics["revenue_growth_rate"] = metrics["revenue_usd_millions"].pct_change()
    metrics["net_income_growth_rate"] = metrics["net_income_usd_millions"].pct_change()
    metrics["gross_margin"] = metrics["gross_profit_usd_millions"] / metrics["revenue_usd_millions"]
    metrics["operating_margin"] = metrics["operating_income_usd_millions"] / metrics["revenue_usd_millions"]
    metrics["net_profit_margin"] = metrics["net_income_usd_millions"] / metrics["revenue_usd_millions"]
    metrics["free_cash_flow_margin"] = metrics["free_cash_flow_usd_millions"] / metrics["revenue_usd_millions"]
    metrics["return_on_equity"] = metrics["net_income_usd_millions"] / metrics["shareholders_equity_usd_millions"]

    return metrics


def load_apple_financial_metrics() -> pd.DataFrame:
    """Load source data and return it with calculated analysis metrics."""
    financials = load_apple_financials()
    return add_calculated_metrics(financials)


def validate_calculated_metrics(metrics: pd.DataFrame) -> dict[str, object]:
    """Return quality checks for calculated financial metrics."""
    missing_values = metrics[PERCENTAGE_COLUMNS].isna().sum()
    first_year = metrics["fiscal_year"].min()
    first_year_metrics = metrics.loc[metrics["fiscal_year"] == first_year].iloc[0]

    expected_missing_growth_fields = {
        "revenue_growth_rate": 1,
        "net_income_growth_rate": 1,
    }
    actual_missing_growth_fields = {
        column: int(missing_values[column])
        for column in expected_missing_growth_fields
        if missing_values[column] > 0
    }

    return {
        "row_count": len(metrics),
        "column_count": len(metrics.columns),
        "percentage_columns": PERCENTAGE_COLUMNS,
        "missing_metric_values": missing_values[missing_values > 0].to_dict(),
        "expected_missing_growth_values": actual_missing_growth_fields == expected_missing_growth_fields,
        "first_year": int(first_year),
        "first_year_revenue_growth_is_missing": pd.isna(first_year_metrics["revenue_growth_rate"]),
        "first_year_net_income_growth_is_missing": pd.isna(first_year_metrics["net_income_growth_rate"]),
    }


def save_processed_metrics(output_path: Path = PROCESSED_DATA_PATH) -> Path:
    """Save calculated metrics to data/processed for downstream project steps."""
    metrics = load_apple_financial_metrics()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output_path, index=False, date_format="%Y-%m-%d")
    return output_path


if __name__ == "__main__":
    apple_metrics = load_apple_financial_metrics()
    validation = validate_calculated_metrics(apple_metrics)
    saved_path = save_processed_metrics()

    print(f"Rows: {validation['row_count']}")
    print(f"Columns: {validation['column_count']}")
    print("Metric columns:", validation["percentage_columns"])
    print("Missing metric values:", validation["missing_metric_values"] or "None")
    print("Expected missing growth values:", validation["expected_missing_growth_values"])
    print(f"Saved processed metrics to: {saved_path}")
