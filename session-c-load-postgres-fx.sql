-- Project 1 (FX) — load fx_tidy.csv into PostgreSQL, idempotent.
-- Database: project1 (create it first, do NOT load into the Session A drill DB)
--   CREATE DATABASE project1;  \c project1
-- Run this file in psql, then load the CSV twice: row count must NOT change.
--
-- Table: fx_rates, natural key (currency, date)
--   rate = units of currency per 1 USD (base USD, Frankfurter / ECB)
--   inverse_rate = 1 / rate ; daily_change_pct is NULL for the first
--   date of each currency in the file ; movement in first/up/down/flat

CREATE TABLE IF NOT EXISTS fx_rates (
    currency         TEXT NOT NULL,
    date             DATE NOT NULL,
    rate             NUMERIC NOT NULL,
    inverse_rate     NUMERIC NOT NULL,
    daily_change_pct NUMERIC,
    movement         TEXT NOT NULL CHECK (movement IN ('first','up','down','flat')),
    PRIMARY KEY (currency, date)
);

-- Staging load: re-runnable, ON CONFLICT does nothing on re-load.
CREATE TEMP TABLE fx_staging (LIKE fx_rates);

\copy fx_staging(currency, date, rate, inverse_rate, daily_change_pct, movement) FROM 'fx_tidy.csv' WITH (FORMAT csv, HEADER true, NULL '')

INSERT INTO fx_rates
SELECT * FROM fx_staging
ON CONFLICT (currency, date) DO NOTHING;

SELECT COUNT(*) AS rows_in_fx_rates FROM fx_rates;
SELECT currency, COUNT(*) AS days, MIN(date) AS first_date, MAX(date) AS last_date
FROM fx_rates GROUP BY currency ORDER BY currency;
