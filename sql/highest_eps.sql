-- Find the fiscal year with Apple's highest diluted EPS.
SELECT
    fiscal_year,
    diluted_eps_usd_per_share
FROM apple_financial_metrics
ORDER BY diluted_eps_usd_per_share DESC
LIMIT 1;
