"""Streamlit dashboard for Apple's annual financial analysis."""

from pathlib import Path
import sqlite3

import pandas as pd
import plotly.graph_objects as go
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


@st.cache_data
def run_sql_query(query: str) -> pd.DataFrame:
    """Run a SQL query against the project SQLite database."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        return pd.read_sql_query(query, connection)


def format_dollars_millions(value: float) -> str:
    """Format USD millions in a readable dashboard style."""
    return f"${value:,.0f}M"


def format_percent(value: float | None) -> str:
    """Format decimal ratios as percentages."""
    if pd.isna(value):
        return "N/A"
    return f"{value * 100:.1f}%"


def format_delta(value: float | None, suffix: str = "%") -> str:
    """Format dashboard deltas while handling the first year."""
    if pd.isna(value):
        return "No prior year"
    return f"{value * 100:+.1f}{suffix} vs. prior year"


def get_selected_year_row(financials: pd.DataFrame, fiscal_year: int) -> pd.Series:
    """Return the financial metrics for one fiscal year."""
    return financials.loc[financials["fiscal_year"] == fiscal_year].iloc[0]


def get_prior_year_row(financials: pd.DataFrame, fiscal_year: int) -> pd.Series | None:
    """Return the prior year row when it exists."""
    prior_year = fiscal_year - 1
    prior_rows = financials.loc[financials["fiscal_year"] == prior_year]
    if prior_rows.empty:
        return None
    return prior_rows.iloc[0]


def add_custom_css() -> None:
    """Apply light custom styling for a finance-dashboard look."""
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }

        [data-testid="stSidebar"] {
            background: #0b1f33;
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        .dashboard-header {
            border: 1px solid #d8dee9;
            border-radius: 8px;
            padding: 16px 20px;
            text-align: center;
            background: linear-gradient(180deg, #ffffff 0%, #f6f8fb 100%);
            margin-bottom: 14px;
        }

        .dashboard-header h1 {
            font-size: 30px;
            margin: 0;
            color: #0f172a;
        }

        .dashboard-header h2 {
            font-size: 20px;
            margin: 4px 0 0 0;
            color: #1f2937;
        }

        .dashboard-header p {
            margin: 4px 0 0 0;
            color: #475569;
        }

        .kpi-card {
            border: 1px solid #d8dee9;
            border-radius: 8px;
            padding: 14px;
            background: #ffffff;
            min-height: 132px;
            box-shadow: 0 1px 4px rgba(15, 23, 42, 0.08);
        }

        .kpi-label {
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            color: #0f172a;
            min-height: 34px;
        }

        .kpi-value {
            font-size: 25px;
            font-weight: 800;
            color: #020617;
            margin-top: 8px;
        }

        .kpi-delta-positive {
            color: #15803d;
            font-size: 14px;
            font-weight: 700;
            margin-top: 8px;
        }

        .kpi-delta-negative {
            color: #b91c1c;
            font-size: 14px;
            font-weight: 700;
            margin-top: 8px;
        }

        .panel {
            border: 1px solid #d8dee9;
            border-radius: 8px;
            padding: 16px;
            background: #ffffff;
            min-height: 100%;
        }

        .panel h3 {
            color: #0f172a;
            font-size: 16px;
            margin-top: 0;
            text-transform: uppercase;
        }

        .sql-box {
            background: #07111f;
            color: #d1fae5;
            border-radius: 8px;
            padding: 14px;
            font-size: 13px;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_sidebar() -> None:
    """Display project context in the sidebar."""
    st.sidebar.markdown("## Apple")
    st.sidebar.markdown("### About This Dashboard")
    st.sidebar.write(
        "This dashboard analyzes Apple Inc.'s audited annual financial performance "
        "from FY2022 through FY2025."
    )

    st.sidebar.markdown("### Company Overview")
    st.sidebar.write("Ticker: AAPL")
    st.sidebar.write("Exchange: Nasdaq")
    st.sidebar.write("Industry: Consumer Technology")
    st.sidebar.write("Fiscal year end: September")

    st.sidebar.markdown("### Data Source")
    st.sidebar.write("FY2022-FY2025 Apple Form 10-K filings.")
    st.sidebar.write("All dollar amounts are in USD millions unless noted.")

    st.sidebar.markdown("### Dashboard Sections")
    st.sidebar.write("Executive Summary")
    st.sidebar.write("Financial Trends")
    st.sidebar.write("Ratio Analysis")
    st.sidebar.write("SQL Insight")
    st.sidebar.write("Management Summary")


def show_header(selected_year: int) -> None:
    """Display the dashboard title area."""
    st.markdown(
        f"""
        <div class="dashboard-header">
            <h1>FINANCIAL PERFORMANCE DASHBOARD</h1>
            <h2>Apple Inc. (AAPL)</h2>
            <p>FY2022 - FY2025 | Selected Year: FY{selected_year}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_kpi_card(label: str, value: str, delta: str, positive: bool = True) -> None:
    """Render one dashboard KPI card."""
    delta_class = "kpi-delta-positive" if positive else "kpi-delta-negative"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="{delta_class}">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_kpi_row(selected_year: pd.Series, prior_year: pd.Series | None) -> None:
    """Display six key performance cards."""
    fiscal_year = int(selected_year["fiscal_year"])
    revenue_growth = selected_year["revenue_growth_rate"]
    net_income_growth = selected_year["net_income_growth_rate"]

    if prior_year is None:
        operating_margin_delta = None
        net_margin_delta = None
        free_cash_flow_delta = None
        roe_delta = None
    else:
        operating_margin_delta = selected_year["operating_margin"] - prior_year["operating_margin"]
        net_margin_delta = selected_year["net_profit_margin"] - prior_year["net_profit_margin"]
        free_cash_flow_delta = (
            selected_year["free_cash_flow_usd_millions"] / prior_year["free_cash_flow_usd_millions"]
        ) - 1
        roe_delta = selected_year["return_on_equity"] - prior_year["return_on_equity"]

    cards = st.columns(6)
    with cards[0]:
        show_kpi_card(
            f"Revenue (FY{fiscal_year})",
            format_dollars_millions(selected_year["revenue_usd_millions"]),
            format_delta(revenue_growth),
            revenue_growth >= 0 if not pd.isna(revenue_growth) else True,
        )
    with cards[1]:
        show_kpi_card(
            f"Net Income (FY{fiscal_year})",
            format_dollars_millions(selected_year["net_income_usd_millions"]),
            format_delta(net_income_growth),
            net_income_growth >= 0 if not pd.isna(net_income_growth) else True,
        )
    with cards[2]:
        show_kpi_card(
            "Operating Margin",
            format_percent(selected_year["operating_margin"]),
            format_delta(operating_margin_delta, " pp"),
            operating_margin_delta >= 0 if operating_margin_delta is not None else True,
        )
    with cards[3]:
        show_kpi_card(
            "Net Margin",
            format_percent(selected_year["net_profit_margin"]),
            format_delta(net_margin_delta, " pp"),
            net_margin_delta >= 0 if net_margin_delta is not None else True,
        )
    with cards[4]:
        show_kpi_card(
            f"Free Cash Flow (FY{fiscal_year})",
            format_dollars_millions(selected_year["free_cash_flow_usd_millions"]),
            format_delta(free_cash_flow_delta),
            free_cash_flow_delta >= 0 if free_cash_flow_delta is not None else True,
        )
    with cards[5]:
        show_kpi_card(
            "Return on Equity",
            format_percent(selected_year["return_on_equity"]),
            format_delta(roe_delta, " pp"),
            roe_delta >= 0 if roe_delta is not None else True,
        )


def build_line_chart(
    financials: pd.DataFrame,
    y_column: str,
    title: str,
    y_label: str,
    color: str,
    value_format: str = "usd_millions",
) -> go.Figure:
    """Create a polished line chart for annual financial trends."""
    if value_format == "percent":
        y_values = financials[y_column] * 100
        labels = [f"{value:.1f}%" for value in y_values]
    elif value_format == "usd_per_share":
        y_values = financials[y_column]
        labels = [f"${value:.2f}" for value in y_values]
    else:
        y_values = financials[y_column]
        labels = [f"${value:,.0f}M" for value in y_values]

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=financials["fiscal_year"],
            y=y_values,
            mode="lines+markers+text",
            line={"color": color, "width": 3},
            marker={"size": 8},
            text=labels,
            textposition="top center",
        )
    )
    figure.update_layout(
        title={"text": title, "x": 0.5, "xanchor": "center"},
        height=315,
        margin={"l": 20, "r": 20, "t": 55, "b": 20},
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis={"title": "Fiscal Year", "dtick": 1, "showgrid": False},
        yaxis={"title": y_label, "gridcolor": "#e5e7eb"},
        showlegend=False,
    )
    return figure


def show_main_charts(financials: pd.DataFrame) -> None:
    """Display the top financial trend charts."""
    chart_columns = st.columns(3)
    chart_columns[0].plotly_chart(
        build_line_chart(financials, "revenue_usd_millions", "Revenue Trend", "USD millions", "#2563eb"),
        use_container_width=True,
    )
    chart_columns[1].plotly_chart(
        build_line_chart(financials, "net_income_usd_millions", "Net Income Trend", "USD millions", "#16a34a"),
        use_container_width=True,
    )
    chart_columns[2].plotly_chart(
        build_line_chart(
            financials,
            "free_cash_flow_usd_millions",
            "Free Cash Flow Trend",
            "USD millions",
            "#eab308",
        ),
        use_container_width=True,
    )


def build_ratio_table(financials: pd.DataFrame) -> pd.DataFrame:
    """Create a year-by-year table of key financial ratios."""
    ratios = {
        "Gross Margin": "gross_margin",
        "Operating Margin": "operating_margin",
        "Net Margin": "net_profit_margin",
        "Free Cash Flow Margin": "free_cash_flow_margin",
        "ROE": "return_on_equity",
    }
    rows = []
    for label, column in ratios.items():
        row = {"Metric": label}
        for _, year_data in financials.iterrows():
            row[f"FY{int(year_data['fiscal_year'])}"] = format_percent(year_data[column])
        rows.append(row)
    return pd.DataFrame(rows)


def build_balance_sheet_mix_chart(selected_year: pd.Series) -> go.Figure:
    """Show liabilities and equity as a simple balance sheet mix view."""
    labels = ["Total Liabilities", "Shareholders' Equity"]
    values = [
        selected_year["total_liabilities_usd_millions"],
        selected_year["shareholders_equity_usd_millions"],
    ]
    figure = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker={"colors": ["#dc2626", "#2563eb"]},
                textinfo="label+percent",
            )
        ]
    )
    figure.update_layout(
        title={"text": "Balance Sheet Mix", "x": 0.5, "xanchor": "center"},
        height=340,
        margin={"l": 10, "r": 10, "t": 55, "b": 10},
        annotations=[
            {
                "text": f"FY{int(selected_year['fiscal_year'])}",
                "x": 0.5,
                "y": 0.5,
                "font_size": 18,
                "showarrow": False,
            }
        ],
    )
    return figure


def show_ratio_and_balance_section(financials: pd.DataFrame, selected_year: pd.Series) -> None:
    """Display ratio analysis, EPS, ROE, and balance sheet mix panels."""
    ratio_panel, eps_panel, roe_panel, balance_panel = st.columns([1.25, 1, 1, 1])

    with ratio_panel:
        st.markdown('<div class="panel"><h3>Key Financial Ratios</h3>', unsafe_allow_html=True)
        st.dataframe(build_ratio_table(financials), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with eps_panel:
        st.plotly_chart(
            build_line_chart(
                financials,
                "diluted_eps_usd_per_share",
                "Diluted EPS Trend",
                "USD/share",
                "#7c3aed",
                "usd_per_share",
            ),
            use_container_width=True,
        )

    with roe_panel:
        st.plotly_chart(
            build_line_chart(financials, "return_on_equity", "ROE Trend", "ROE %", "#0f766e", "percent"),
            use_container_width=True,
        )

    with balance_panel:
        st.plotly_chart(build_balance_sheet_mix_chart(selected_year), use_container_width=True)


def show_sql_and_summary(financials: pd.DataFrame, selected_year: pd.Series) -> None:
    """Display SQL proof and management-style summary."""
    sql_column, summary_column = st.columns([1.35, 1])
    sql_query = """
SELECT
    fiscal_year,
    revenue_usd_millions
FROM apple_financial_metrics
ORDER BY revenue_usd_millions DESC
LIMIT 1;
""".strip()
    sql_result = run_sql_query(sql_query)

    with sql_column:
        st.markdown('<div class="panel"><h3>SQL Insight Example</h3>', unsafe_allow_html=True)
        st.markdown(f'<div class="sql-box">{sql_query}</div>', unsafe_allow_html=True)
        st.dataframe(sql_result, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    latest_year = int(financials["fiscal_year"].max())
    revenue_growth = format_percent(selected_year["revenue_growth_rate"])
    net_margin = format_percent(selected_year["net_profit_margin"])
    roe = format_percent(selected_year["return_on_equity"])

    with summary_column:
        st.markdown(
            f"""
            <div class="panel">
                <h3>Management Summary</h3>
                <p>
                    In FY{int(selected_year['fiscal_year'])}, Apple generated
                    <strong>{format_dollars_millions(selected_year['revenue_usd_millions'])}</strong>
                    in revenue and <strong>{format_dollars_millions(selected_year['net_income_usd_millions'])}</strong>
                    in net income.
                </p>
                <p>
                    Revenue growth was <strong>{revenue_growth}</strong>, net profit margin was
                    <strong>{net_margin}</strong>, and ROE was <strong>{roe}</strong>.
                </p>
                <p>
                    The dashboard is currently filtered to FY{int(selected_year['fiscal_year'])};
                    the most recent year in the dataset is FY{latest_year}.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    """Run the Streamlit dashboard."""
    st.set_page_config(page_title="Apple Financial Analysis", layout="wide")
    add_custom_css()

    financials = load_financial_metrics()
    fiscal_years = financials["fiscal_year"].tolist()

    show_sidebar()

    selected_fiscal_year = st.selectbox(
        "Year",
        fiscal_years,
        index=len(fiscal_years) - 1,
    )
    selected_year = get_selected_year_row(financials, selected_fiscal_year)
    prior_year = get_prior_year_row(financials, selected_fiscal_year)

    show_header(selected_fiscal_year)
    show_kpi_row(selected_year, prior_year)
    show_main_charts(financials)
    show_ratio_and_balance_section(financials, selected_year)
    show_sql_and_summary(financials, selected_year)


if __name__ == "__main__":
    main()
