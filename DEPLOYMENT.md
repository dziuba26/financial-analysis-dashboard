# Deployment Guide

This project is ready to deploy with Streamlit Community Cloud.

## Recommended Platform

Use Streamlit Community Cloud because this project is already a Streamlit app and the repository already has the files Community Cloud expects:

- `app.py`
- `requirements.txt`
- `database/financial_analysis.sqlite`
- `data/`
- `sql/`

## Deploy Steps

1. Go to:

```text
https://share.streamlit.io
```

2. Sign in with GitHub.

3. Click `Create app`.

4. Choose `Yup, I have an app`.

5. Enter:

```text
Repository: dziuba26/financial-analysis-dashboard
Branch: main
Main file path: app.py
```

6. Open `Advanced settings` and use Python 3.12.

This matches Streamlit Community Cloud's documented default and keeps the app on a stable Python version for pandas, Plotly, and Streamlit.

7. Choose an app URL if Streamlit gives you the option.

Recommended URL:

```text
apple-financial-analysis-dashboard
```

8. Click `Deploy`.

## After Deployment

Once the app is live, copy the public Streamlit URL and update the `Live Demo` section in `README.md`.

The URL will usually look like:

```text
https://your-app-name.streamlit.app
```

## Resume Bullet

Use this version as a starting point:

```text
Built and deployed an interactive Apple financial analysis dashboard using Python, pandas, SQLite, SQL, Streamlit, Plotly, and Excel to analyze FY2022-FY2025 financial performance.
```

## Troubleshooting

If the app fails to deploy, check these first:

- `requirements.txt` is in the repository root.
- `app.py` is the selected main file path.
- The GitHub repository is public or connected to Streamlit.
- `database/financial_analysis.sqlite` is committed to GitHub.
- The app runs locally with `streamlit run app.py`.
- Python 3.12 is selected in Streamlit Community Cloud advanced settings.
