"""Streamlit dashboard for Apple's annual financial analysis."""

from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_ROOT / "database" / "financial_analysis.sqlite"
TABLE_NAME = "apple_financial_metrics"


@st.cache_data
def load_financial_metrics() -> pd.DataFrame:
    """Load Apple financial metrics from SQLite for dashboard visuals."""
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        ORDER BY fiscal_year
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        financials = pd.read_sql_query(query, connection)

    financials["period_end"] = pd.to_datetime(financials["period_end"])
    return financials


def format_dollars_millions(value: float) -> str:
    """Format USD millions in a readable dashboard style."""
    return f"${value:,.0f}M"


def format_percent(value: float | None) -> str:
    """Format decimal ratios as percentages."""
    if pd.isna(value):
        return "N/A"
    return f"{value * 100:.2f}%"


def build_trend_chart(financials: pd.DataFrame, y_column: str, title: str, y_label: str):
    """Create a consistent annual trend chart."""
    chart = px.line(
        financials,
        x="fiscal_year",
        y=y_column,
        markers=True,
        title=title,
        labels={"fiscal_year": "Fiscal Year", y_column: y_label},
    )
    chart.update_layout(
        height=320,
        margin={"l": 20, "r": 20, "t": 55, "b": 20},
        xaxis={"dtick": 1},
    )
    return chart


def get_selected_year_row(financials: pd.DataFrame, fiscal_year: int) -> pd.Series:
    """Return the financial metrics for one fiscal year."""
    return financials.loc[financials["fiscal_year"] == fiscal_year].iloc[0]


def show_executive_summary(selected_year: pd.Series) -> None:
    """Display the main dashboard metrics for the selected fiscal year."""
    st.subheader(f"Executive Summary: FY{selected_year['fiscal_year']}")

    revenue, net_income, eps, roe = st.columns(4)
    revenue.metric("Revenue", format_dollars_millions(selected_year["revenue_usd_millions"]))
    net_income.metric("Net Income", format_dollars_millions(selected_year["net_income_usd_millions"]))
    eps.metric("Diluted EPS", f"${selected_year['diluted_eps_usd_per_share']:.2f}")
    roe.metric("ROE", format_percent(selected_year["return_on_equity"]))


def show_charts(financials: pd.DataFrame) -> None:
    """Display the required MVP trend charts."""
    st.subheader("Financial Trends")

    left, right = st.columns(2)
    left.plotly_chart(
        build_trend_chart(financials, "revenue_usd_millions", "Revenue Trend", "Revenue (USD millions)"),
        use_container_width=True,
    )
    right.plotly_chart(
        build_trend_chart(financials, "net_income_usd_millions", "Net Income Trend", "Net Income (USD millions)"),
        use_container_width=True,
    )

    left, right = st.columns(2)
    left.plotly_chart(
        build_trend_chart(financials, "diluted_eps_usd_per_share", "Diluted EPS Trend", "Diluted EPS"),
        use_container_width=True,
    )
    right.plotly_chart(
        build_trend_chart(financials, "return_on_equity", "ROE Trend", "ROE"),
        use_container_width=True,
    )


def show_analyst_observations(financials: pd.DataFrame, selected_year: pd.Series) -> None:
    """Display concise analyst observations for the selected year."""
    st.subheader("Analyst Observations")

    latest_year = int(financials["fiscal_year"].max())
    highest_revenue_year = financials.loc[financials["revenue_usd_millions"].idxmax()]
    highest_eps_year = financials.loc[financials["diluted_eps_usd_per_share"].idxmax()]

    observations = [
        (
            f"FY{int(highest_revenue_year['fiscal_year'])} had the highest revenue "
            f"at {format_dollars_millions(highest_revenue_year['revenue_usd_millions'])}."
        ),
        (
            f"FY{int(highest_eps_year['fiscal_year'])} had the highest diluted EPS "
            f"at ${highest_eps_year['diluted_eps_usd_per_share']:.2f}."
        ),
        (
            f"Selected-year net profit margin was "
            f"{format_percent(selected_year['net_profit_margin'])}."
        ),
    ]

    if int(selected_year["fiscal_year"]) == latest_year:
        observations.append(
            f"Latest-year revenue growth was {format_percent(selected_year['revenue_growth_rate'])}."
        )

    for observation in observations:
        st.markdown(f"- {observation}")


def main() -> None:
    """Run the Streamlit dashboard."""
    st.set_page_config(page_title="Apple Financial Analysis", layout="wide")

    financials = load_financial_metrics()
    fiscal_years = financials["fiscal_year"].tolist()

    st.title("Apple Financial Analysis Dashboard")
    st.caption("Annual financial metrics from FY2022-FY2025 Form 10-K data.")

    selected_fiscal_year = st.selectbox(
        "Fiscal Year",
        fiscal_years,
        index=len(fiscal_years) - 1,
    )
    selected_year = get_selected_year_row(financials, selected_fiscal_year)

    show_executive_summary(selected_year)
    show_charts(financials)
    show_analyst_observations(financials, selected_year)


if __name__ == "__main__":
    main()
