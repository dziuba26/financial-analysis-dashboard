-- Find the fiscal year with Apple's highest return on equity.
-- ROE uses ending shareholders' equity in this project.
SELECT
    fiscal_year,
    ROUND(return_on_equity * 100, 2) AS roe_pct
FROM apple_financial_metrics
ORDER BY return_on_equity DESC
LIMIT 1;
