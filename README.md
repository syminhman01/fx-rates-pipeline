# **FX Rates Pipeline — Project 1 v0**  
FX rates data pipeline: Frankfurter API (ECB) -> Python -> PostgreSQL.  
## **Source decision**  
Project 1 v0: FX rates, Frankfurter API, base USD, EUR/GBP/JPY,  
 because of pipeline / time-series / repeatable incremental ingest,  
 in a finance domain. Open-Meteo was dropped on 09/11/2026.  
- Source: Frankfurter API (ECB reference rates), free, no key.  
- Base: USD. Currencies: EUR, GBP, JPY. No VND — Frankfurter has none.  
- Window v0: 2026-10-12 to 2026-10-20 (calendar).  
   FX has no weekend rates, so this gives 7 business days  
   (12, 13, 14, 15, 16, 19, 20 Oct) x 3 currencies = 21 rows.  
- Natural key: (currency, date).  
- Columns: currency,date,rate,inverse_rate,daily_change_pct,movement  
- inverse_rate = round(1 / rate, 6)  
- daily_change_pct vs the previous business day of the same  
     currency; blank on the first day, movement = 'first'.  
## **Pipeline**  
1. Ingest: python session-c-fx-starter.py -> fx_tidy.csv (21 rows)  
2. Check: python session-c-project-first-fx-checker.py -> 6/6  
3. Load: PostgreSQL database project1, table fx_rates,  
    staging + ON CONFLICT (currency, date) DO NOTHING.  
    Re-running the load must not change the row count (21).  
4. Analyse: session-c-queries-fx.sql — avg rate, min/max/range,  
    biggest single-day move per currency.  
## **Structure**  
v0 is intentionally flat, so the checker and the load SQL work  
 with relative paths as verified (checker 6/6):  
.  
├── README.md  
├── session-c-fx-starter.py  
├── session-c-project-first-fx-checker.py  
├── session-c-fx-sample.csv  
├── fx_tidy.csv  
├── session-c-load-postgres-fx.sql  
└── session-c-queries-fx.sql  
Planned structure — refactor at the start of Week 2 Session C  
 (21 -> 42 rows), then add dim/fact modelling, Docker and pytest  
 in Dec 2026:  
├── src/            # fetch_fx.py (starter, renamed on refactor)  
├── sql/            # schema.sql, load.sql, analysis.sql  
│   └── models/     # dim_currency, fact_fx_daily, dim_date  
├── data/           # fx_tidy.csv  
├── tests/          # pytest (from Dec)  
├── docker/         # docker-compose.yml for PostgreSQL (from Dec)  
└── docs/           # decisions.md  
## **Results (v0)**  
- Rows loaded: 21  
- Avg rate: EUR 0.8921, GBP 0.7526, JPY 158.22  
- Biggest single-day move: EUR 2026-10-16, -0.4001%;  
   GBP 2026-10-16, -0.6650%; JPY 2026-10-13, -0.3026%.  
   
