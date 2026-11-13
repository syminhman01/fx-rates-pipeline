-- Project 1 (FX) — 3 analysis queries, Week 1 (21 rows).
-- Run in database project1, after loading fx_tidy.csv.
-- Cross-check each result against fx_tidy.csv before committing.
--
-- Expected (verified 2026-11-09 from the Frankfurter API):
--   Q1 avg rate: EUR 0.8921, GBP 0.7526, JPY 158.22
--   Q2 min/max:  EUR 0.88865 / 0.89437 ; GBP 0.74925 / 0.75555 ; JPY 157.98 / 158.60
--   Q3 biggest single-day move (by |daily_change_pct|):
--     EUR 2026-10-16, -0.4001% ; GBP 2026-10-16, -0.6650% ; JPY 2026-10-13, -0.3026%

-- Q1: average rate per currency
SELECT currency,
       ROUND(AVG(rate), 4) AS avg_rate,
       COUNT(*) AS days
FROM fx_rates
GROUP BY currency
ORDER BY currency;

-- Q2: min / max rate and range per currency
SELECT currency,
       MIN(rate) AS min_rate,
       MAX(rate) AS max_rate,
       ROUND(MAX(rate) - MIN(rate), 4) AS range_rate
FROM fx_rates
GROUP BY currency
ORDER BY currency;

-- Q3: biggest single-day move per currency (largest absolute % change)
SELECT DISTINCT ON (currency)
       currency, date, daily_change_pct, movement
FROM fx_rates
WHERE daily_change_pct IS NOT NULL
ORDER BY currency, ABS(daily_change_pct) DESC;
