-- Calculate Apple's average year-over-year revenue growth.
-- FY2022 is excluded because it has no prior year in this dataset.
SELECT
    ROUND(AVG(revenue_growth_rate) * 100, 2) AS average_revenue_growth_pct
FROM apple_financial_metrics
WHERE revenue_growth_rate IS NOT NULL;
