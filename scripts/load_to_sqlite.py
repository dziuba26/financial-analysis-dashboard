"""Load processed Apple financial metrics into SQLite.

This script takes the processed CSV created by calculate_metrics.py and stores it
as a queryable SQLite table. The raw audited CSV is not modified.
"""

from pathlib import Path
import sqlite3
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from scripts.calculate_metrics import PROCESSED_DATA_PATH

DATABASE_PATH = PROJECT_ROOT / "database" / "financial_analysis.sqlite"
TABLE_NAME = "apple_financial_metrics"

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

REAL_COLUMNS = [
    "diluted_eps_usd_per_share",
    "revenue_growth_rate",
    "net_income_growth_rate",
    "gross_margin",
    "operating_margin",
    "net_profit_margin",
    "free_cash_flow_margin",
    "return_on_equity",
]

SQLITE_COLUMN_TYPES = {
    "period_end": "TEXT",
    **{column: "INTEGER" for column in INTEGER_COLUMNS},
    **{column: "REAL" for column in REAL_COLUMNS},
}


def load_processed_metrics(csv_path: Path = PROCESSED_DATA_PATH) -> pd.DataFrame:
    """Read the processed metrics CSV that will be loaded into SQLite."""
    metrics = pd.read_csv(csv_path)
    metrics["period_end"] = pd.to_datetime(metrics["period_end"]).dt.strftime("%Y-%m-%d")
    return metrics


def write_metrics_to_sqlite(
    metrics: pd.DataFrame,
    database_path: Path = DATABASE_PATH,
    table_name: str = TABLE_NAME,
) -> Path:
    """Replace the SQLite table with the latest processed metrics."""
    database_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_path) as connection:
        metrics.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False,
            dtype=SQLITE_COLUMN_TYPES,
        )
        connection.execute(
            f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_fiscal_year "
            f"ON {table_name} (fiscal_year)"
        )

    return database_path


def validate_sqlite_table(
    database_path: Path = DATABASE_PATH,
    table_name: str = TABLE_NAME,
) -> dict[str, object]:
    """Return simple checks proving the SQLite table loaded correctly."""
    with sqlite3.connect(database_path) as connection:
        row_count = connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        fiscal_years = [
            row[0]
            for row in connection.execute(
                f"SELECT fiscal_year FROM {table_name} ORDER BY fiscal_year"
            ).fetchall()
        ]
        columns = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        null_growth_rows = connection.execute(
            f"""
            SELECT COUNT(*)
            FROM {table_name}
            WHERE revenue_growth_rate IS NULL
               OR net_income_growth_rate IS NULL
            """
        ).fetchone()[0]

    return {
        "database_path": str(database_path),
        "table_name": table_name,
        "row_count": row_count,
        "column_count": len(columns),
        "fiscal_years": fiscal_years,
        "null_growth_rows": null_growth_rows,
        "columns": [(column[1], column[2]) for column in columns],
    }


def main() -> None:
    """Load processed Apple metrics into SQLite and print validation checks."""
    metrics = load_processed_metrics()
    database_path = write_metrics_to_sqlite(metrics)
    validation = validate_sqlite_table(database_path)

    print(f"Database: {validation['database_path']}")
    print(f"Table: {validation['table_name']}")
    print(f"Rows: {validation['row_count']}")
    print(f"Columns: {validation['column_count']}")
    print(f"Fiscal years: {validation['fiscal_years']}")
    print(f"Rows with missing growth values: {validation['null_growth_rows']}")
    print("\nSQLite columns:")
    for column_name, column_type in validation["columns"]:
        print(f"- {column_name}: {column_type}")


if __name__ == "__main__":
    main()
