-- Show Apple's annual financial results and key calculated metrics.
SELECT
    fiscal_year,
    period_end,
    revenue_usd_millions,
    net_income_usd_millions,
    diluted_eps_usd_per_share,
    ROUND(revenue_growth_rate * 100, 2) AS revenue_growth_pct,
    ROUND(net_income_growth_rate * 100, 2) AS net_income_growth_pct,
    ROUND(return_on_equity * 100, 2) AS roe_pct
FROM apple_financial_metrics
ORDER BY fiscal_year;
