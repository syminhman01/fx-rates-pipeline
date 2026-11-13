"""Project 1 v0 (FX) — starter: fetch Frankfurter FX rates, write tidy CSV.

Source: Frankfurter API (ECB reference rates), free, no key, no signup.
  https://api.frankfurter.dev/v1/
  Example: https://api.frankfurter.dev/v1/2026-10-12..2026-10-20?base=USD&symbols=EUR,JPY,GBP

Spec (Week 1):
  base = USD, currencies = EUR, GBP, JPY
  window = 2026-10-12 .. 2026-10-20 (calendar)
  => 7 business days only (Sat/Sun 17-18 Oct have NO FX rates),
     3 currencies x 7 days = 21 rows, key (currency, date)
  output: fx_tidy.csv, columns:
    currency,date,rate,inverse_rate,daily_change_pct,movement
  - rate: as returned by the API (units of currency per 1 USD)
  - inverse_rate = round(1 / rate, 6)
  - daily_change_pct = round((rate - prev_rate) / prev_rate * 100, 4),
    blank for the first date of each currency in the file
  - movement: 'first' for the first date, else 'up' / 'down' / 'flat'
  - sort: currency A-Z, then date ascending

Run: python session-c-fx-starter.py
  -> writes fx_tidy.csv in the same folder.
Then run the checker: python session-c-project-first-fx-checker.py
"""
import csv
import json
import urllib.request

BASE = "USD"
CURRENCIES = ["EUR", "GBP", "JPY"]
START = "2026-10-12"
END = "2026-10-20"
OUT = "fx_tidy.csv"


def fetch(start, end):
    url = (
        f"https://api.frankfurter.dev/v1/{start}..{end}"
        f"?base={BASE}&symbols={','.join(CURRENCIES)}"
    )
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.load(resp)


def tidy(data):
    rates = data["rates"]
    rows = []
    prev = {}
    for date in sorted(rates):
        for cur in sorted(rates[date]):
            rate = rates[date][cur]
            inv = round(1 / rate, 6)
            if cur in prev:
                ch = round((rate - prev[cur]) / prev[cur] * 100, 4)
                mv = "up" if ch > 0 else "down" if ch < 0 else "flat"
                ch_s = f"{ch:.4f}"
            else:
                ch_s = ""
                mv = "first"
            rows.append([cur, date, rate, inv, ch_s, mv])
            prev[cur] = rate
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


def main():
    data = fetch(START, END)
    rows = tidy(data)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["currency", "date", "rate", "inverse_rate",
                    "daily_change_pct", "movement"])
        w.writerows(rows)
    print(f"Wrote {OUT}: {len(rows)} rows")


if __name__ == "__main__":
    main()
