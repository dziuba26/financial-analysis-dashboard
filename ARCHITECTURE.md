# ARCHITECTURE.md

# High Level Architecture

Public Financial Data

↓

CSV

↓

pandas

↓

SQLite

↓

SQL Queries

↓

Streamlit Dashboard

↓

Excel Export

---

# Repository Structure

data/

Contains raw and processed financial data.

database/

SQLite database.

scripts/

Data cleaning and utility scripts.

sql/

Reusable SQL queries.

reports/

Generated Excel files.

images/

Dashboard screenshots.

---

# Data Flow

1. Import financial data.
2. Clean data with pandas.
3. Store clean data in SQLite.
4. Query data using SQL.
5. Display results in Streamlit.
6. Export results to Excel.

---

# Design Principles

Keep data immutable.

Separate raw data from processed data.

Separate calculations from visualization.

Avoid duplicated logic.

Every chart should originate from queried data rather than manually entered values.

---

# Desired Characteristics

Simple

Readable

Professional

Maintainable

Finance-first

Interview-ready
