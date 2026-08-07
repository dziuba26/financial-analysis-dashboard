-- Find the fiscal year with Apple's highest revenue.
SELECT
    fiscal_year,
    revenue_usd_millions
FROM apple_financial_metrics
ORDER BY revenue_usd_millions DESC
LIMIT 1;
