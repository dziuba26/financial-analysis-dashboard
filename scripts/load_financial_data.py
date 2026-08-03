"""Load and validate Apple's annual financial statement dataset.

The CSV in data/raw is treated as the source of truth. This module standardizes
column names for Python code, but it does not modify the source file or change
reported financial values.
"""

from pathlib import Path

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_float_dtype, is_integer_dtype

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "apple_financials_2022_2025_units.csv"

COLUMN_NAME_MAP = {
    "Fiscal Year": "fiscal_year",
    "Period End": "period_end",
    "Revenue (USD millions)": "revenue_usd_millions",
    "Gross Profit (USD millions)": "gross_profit_usd_millions",
    "Operating Income (USD millions)": "operating_income_usd_millions",
    "Net Income (USD millions)": "net_income_usd_millions",
    "Diluted EPS (USD/share)": "diluted_eps_usd_per_share",
    "Operating Cash Flow (USD millions)": "operating_cash_flow_usd_millions",
    "Capital Expenditures (USD millions)": "capital_expenditures_usd_millions",
    "Free Cash Flow (USD millions)": "free_cash_flow_usd_millions",
    "Cash & Equivalents (USD millions)": "cash_and_equivalents_usd_millions",
    "Marketable Securities (USD millions)": "marketable_securities_usd_millions",
    "Total Current Assets (USD millions)": "total_current_assets_usd_millions",
    "Total Assets (USD millions)": "total_assets_usd_millions",
    "Total Current Liabilities (USD millions)": "total_current_liabilities_usd_millions",
    "Total Liabilities (USD millions)": "total_liabilities_usd_millions",
    "Shareholders' Equity (USD millions)": "shareholders_equity_usd_millions",
    "Long-Term Debt (USD millions)": "long_term_debt_usd_millions",
    "R&D Expense (USD millions)": "research_and_development_expense_usd_millions",
    "SG&A Expense (USD millions)": "selling_general_and_admin_expense_usd_millions",
    "Share Repurchases (USD millions)": "share_repurchases_usd_millions",
    "Dividends Paid (USD millions)": "dividends_paid_usd_millions",
}

INTEGER_COLUMNS = [
    "fiscal_year",
    "revenue_usd_millions",
    "gross_profit_usd_millions",
    "operating_income_usd_millions",
    "net_income_usd_millions",
    "operating_cash_flow_usd_millions",
    "capital_expenditures_usd_millions",
    "free_cash_flow_usd_millions",
    "cash_and_equivalents_usd_millions",
    "marketable_securities_usd_millions",
    "total_current_assets_usd_millions",
    "total_assets_usd_millions",
    "total_current_liabilities_usd_millions",
    "total_liabilities_usd_millions",
    "shareholders_equity_usd_millions",
    "long_term_debt_usd_millions",
    "research_and_development_expense_usd_millions",
    "selling_general_and_admin_expense_usd_millions",
    "share_repurchases_usd_millions",
    "dividends_paid_usd_millions",
]

FLOAT_COLUMNS = ["diluted_eps_usd_per_share"]
EXPECTED_COLUMNS = list(COLUMN_NAME_MAP.values())


def load_apple_financials(csv_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load Apple's annual financial data with clean Python-friendly columns."""
    raw_data = pd.read_csv(csv_path)
    missing_columns = set(COLUMN_NAME_MAP) - set(raw_data.columns)
    extra_columns = set(raw_data.columns) - set(COLUMN_NAME_MAP)

    if missing_columns or extra_columns:
        raise ValueError(
            "Unexpected CSV columns. "
            f"Missing: {sorted(missing_columns)}. Extra: {sorted(extra_columns)}."
        )

    financials = raw_data.rename(columns=COLUMN_NAME_MAP)
    financials["period_end"] = pd.to_datetime(financials["period_end"], format="%Y-%m-%d")

    for column in INTEGER_COLUMNS:
        financials[column] = financials[column].astype("int64")

    for column in FLOAT_COLUMNS:
        financials[column] = financials[column].astype("float64")

    return financials


def validate_apple_financials(financials: pd.DataFrame) -> dict[str, object]:
    """Return data quality checks for the Apple annual financial dataset."""
    missing_values = financials.isna().sum()
    duplicate_years = financials[financials["fiscal_year"].duplicated()]["fiscal_year"].tolist()
    expected_years = [2022, 2023, 2024, 2025]
    actual_years = financials["fiscal_year"].tolist()

    type_checks = {
        "fiscal_year_is_integer": is_integer_dtype(financials["fiscal_year"]),
        "period_end_is_datetime": is_datetime64_any_dtype(financials["period_end"]),
        "integer_columns_are_integer": all(is_integer_dtype(financials[column]) for column in INTEGER_COLUMNS),
        "eps_is_float": is_float_dtype(financials["diluted_eps_usd_per_share"]),
    }

    return {
        "row_count": len(financials),
        "column_count": len(financials.columns),
        "columns": financials.columns.tolist(),
        "dtypes": {column: str(dtype) for column, dtype in financials.dtypes.items()},
        "missing_values": missing_values[missing_values > 0].to_dict(),
        "duplicate_fiscal_years": duplicate_years,
        "expected_fiscal_years_present": actual_years == expected_years,
        "type_checks": type_checks,
    }


if __name__ == "__main__":
    apple_financials = load_apple_financials()
    validation = validate_apple_financials(apple_financials)

    print(f"Rows: {validation['row_count']}")
    print(f"Columns: {validation['column_count']}")
    print("Missing values:", validation["missing_values"] or "None")
    print("Duplicate fiscal years:", validation["duplicate_fiscal_years"] or "None")
    print("Expected fiscal years present:", validation["expected_fiscal_years_present"])
    print("Type checks:", validation["type_checks"])
    print("\nColumn dtypes:")
    for column, dtype in validation["dtypes"].items():
        print(f"- {column}: {dtype}")
