# Financial Analysis Dashboard

A finance-first portfolio project that uses **Excel, SQL, Python, SQLite, pandas, Plotly, and Streamlit** to analyze Apple Inc.'s annual financial performance.

The current MVP focuses on **Apple Inc.** using audited annual financial statement data from FY2022-FY2025 Form 10-K filings.

## Project Goal

The goal is to show a practical analyst workflow:

```text
Audited financial data
-> raw CSV
-> pandas cleaning
-> calculated financial metrics
-> SQLite database
-> reusable SQL queries
-> Streamlit dashboard
-> Excel report
```

This project is designed for Financial Analyst and Wealth Management internship interviews. It prioritizes clear analysis, traceable data, and tools commonly used in finance.

## Current Status

Completed:

- raw Apple financial dataset
- pandas data-loading module
- calculated financial metrics
- processed metrics CSV
- SQLite database
- reusable SQL queries
- Streamlit dashboard
- Excel workbook export

Remaining:

- dashboard screenshots
- final README screenshot section
- final review and polish

## Key Deliverables

- Streamlit dashboard: `app.py`
- Excel workbook: `reports/apple_financial_analysis_2022_2025.xlsx`
- SQLite database: `database/financial_analysis.sqlite`
- raw dataset: `data/raw/apple_financials_2022_2025_units.csv`
- processed metrics: `data/processed/apple_financial_metrics_2022_2025.csv`
- reusable SQL queries: `sql/`

## Financial Metrics

The project currently analyzes:

- revenue
- net income
- diluted EPS
- gross margin
- operating margin
- net profit margin
- free cash flow margin
- revenue growth
- net income growth
- return on equity

ROE is calculated using ending shareholders' equity:

```text
ROE = net income / shareholders' equity
```

FY2022 growth rates are blank because FY2022 is the first year in the dataset and has no prior year for comparison.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Rebuild The Data Pipeline

Run these commands from the project root.

Create the processed metrics CSV:

```bash
python scripts/calculate_metrics.py
```

Load the processed metrics into SQLite:

```bash
python scripts/load_to_sqlite.py
```

Export the Excel workbook:

```bash
python scripts/export_excel_report.py
```

Run the Streamlit dashboard:

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## SQL Queries

The `sql/` folder contains reusable SQL questions:

- `yearly_results.sql`
- `highest_revenue_year.sql`
- `average_revenue_growth.sql`
- `highest_roe.sql`
- `highest_eps.sql`

Example:

```bash
sqlite3 -header -column database/financial_analysis.sqlite < sql/yearly_results.sql
```

## Project Structure

```text
data/
  raw/          original source data
  processed/    cleaned data with calculated metrics

database/       SQLite database
reports/        generated Excel workbook
scripts/        Python data pipeline scripts
sql/            reusable SQL queries
images/         dashboard screenshots
```

## Data Integrity

The raw CSV is treated as the source of truth. The project does not modify audited financial values. Calculations are added in the processed dataset and can be traced back to the original raw data.

## Interview Summary

This project demonstrates that I can take public financial statement data, clean it with Python, calculate useful financial metrics, store the results in SQLite, query the database with SQL, and present the analysis in both an interactive dashboard and Excel workbook.
