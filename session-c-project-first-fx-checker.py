"""Checker for Week 1 Session C (FX) — reads fx_tidy.csv only, no answers in code.

Run: python session-c-project-first-fx-checker.py
Pass (6/6) when:
  1. header is exactly currency,date,rate,inverse_rate,daily_change_pct,movement
  2. 21 rows, currencies exactly {EUR, GBP, JPY}, 7 dates each
  3. dates are business days in 2026-10-12..2026-10-20 (no Sat/Sun), sorted per currency
  4. no duplicate (currency, date)
  5. inverse_rate == round(1/rate, 6) within 0.000001
  6. daily_change_pct / movement match the previous row of the same currency
     (first row per currency: blank change, movement 'first')
"""
import csv
import sys
from pathlib import Path

FILE = Path(__file__).with_name("fx_tidy.csv")
EXPECTED_HEADER = ["currency", "date", "rate", "inverse_rate",
                   "daily_change_pct", "movement"]
EXPECTED_DATES = ["2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15",
                  "2026-10-16", "2026-10-19", "2026-10-20"]


def fail(msg):
    print(f"FAIL: {msg}")
    return False


def main():
    ok = 0
    if not FILE.exists():
        print(f"FAIL: {FILE.name} not found in this folder")
        return 1

    with open(FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        with open(FILE, newline="", encoding="utf-8") as f2:
            header = next(csv.reader(f2))

    if header == EXPECTED_HEADER:
        print("1/6 header OK"); ok += 1
    else:
        fail(f"header is {header}, expected {EXPECTED_HEADER}")

    if len(rows) == 21 and {r["currency"] for r in rows} == {"EUR", "GBP", "JPY"}:
        print("2/6 21 rows, 3 currencies OK"); ok += 1
    else:
        fail(f"{len(rows)} rows, currencies {[r['currency'] for r in rows]}")

    dates_ok = True
    for cur in ["EUR", "GBP", "JPY"]:
        ds = [r["date"] for r in rows if r["currency"] == cur]
        if ds != EXPECTED_DATES:
            dates_ok = False
            fail(f"{cur} dates {ds}, expected {EXPECTED_DATES}")
    if dates_ok:
        print("3/6 dates OK (7 business days, no weekend)"); ok += 1

    if len({(r["currency"], r["date"]) for r in rows}) == 21:
        print("4/6 no duplicate (currency, date) OK"); ok += 1
    else:
        fail("duplicate (currency, date) found")

    inv_ok = True
    for r in rows:
        try:
            if abs(float(r["inverse_rate"]) - round(1 / float(r["rate"]), 6)) > 1e-6:
                inv_ok = False
                fail(f"inverse_rate wrong at {r['currency']} {r['date']}: {r['inverse_rate']}")
                break
        except ValueError:
            inv_ok = False
            fail(f"non-numeric rate/inverse at {r}")
            break
    if inv_ok:
        print("5/6 inverse_rate OK"); ok += 1

    ch_ok = True
    for cur in ["EUR", "GBP", "JPY"]:
        cr = [r for r in rows if r["currency"] == cur]
        for i, r in enumerate(cr):
            if i == 0:
                if r["daily_change_pct"] != "" or r["movement"] != "first":
                    ch_ok = False
                    fail(f"{cur} first row must be blank change + 'first', got {r}")
            else:
                prev = float(cr[i - 1]["rate"])
                exp = round((float(r["rate"]) - prev) / prev * 100, 4)
                if abs(float(r["daily_change_pct"]) - exp) > 0.0001:
                    ch_ok = False
                    fail(f"{cur} {r['date']} change {r['daily_change_pct']}, expected {exp:.4f}")
                    break
                exp_mv = "up" if exp > 0 else "down" if exp < 0 else "flat"
                if r["movement"] != exp_mv:
                    ch_ok = False
                    fail(f"{cur} {r['date']} movement {r['movement']}, expected {exp_mv}")
                    break
        if not ch_ok:
            break
    if ch_ok:
        print("6/6 daily_change_pct + movement OK"); ok += 1

    print(f"\n{ok}/6 — {'PASS' if ok == 6 else 'fix the FAIL lines above, then re-run'}")
    return 0 if ok == 6 else 1


if __name__ == "__main__":
    sys.exit(main())
