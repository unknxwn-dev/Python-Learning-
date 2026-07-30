"""
newsbot.py - Dukascopy Data Collector
- reads ForexScrape.CSV (UTC event times)
- converts to Zurich time
- pulls 1-s ticks from Dukascopy for 10 min before → 30 min after
- tests base-currency pairs
- outputs one big JSON with all reactions
"""

import datetime as dt
try:
    import lz4.frame
    LZ4_AVAILABLE = True
except ImportError:
    LZ4_AVAILABLE = False
    print("Warning: lz4 not available")
import pandas as pd
import requests
import struct
import os
import time
from tqdm import tqdm
from typing import List, Dict

# ---------- CONFIG -------------------------------------------------
DUKASCOPY_TZ = dt.timezone(dt.timedelta(hours=2))  # Zurich / Geneva
CSV_FILE = "ForexScrape.CSV"
OUTPUT_FILE = "dukascopy_all_reactions.csv"

# ---------- PAIR MAPPINGS -----------------------------------------
# which pairs to test for each currency
PAIR_MAP = {
    "USD": ["USD/GBP", "USD/CAD", "USD/AUD", "USD/JPY", "USD/EUR", "USD/CHF", "USD/NZD"],
    "EUR": ["EUR/USD", "EUR/GBP", "EUR/JPY", "EUR/CHF", "EUR/CAD", "EUR/AUD", "EUR/NZD"],
    "GBP": ["GBP/USD", "GBP/JPY", "GBP/CHF", "GBP/CAD", "GBP/AUD", "GBP/EUR", "GBP/NZD"],
    "JPY": ["JPY/USD", "JPY/EUR", "JPY/GBP", "JPY/AUD", "JPY/CAD", "JPY/CHF", "JPY/NZD"],
    "AUD": ["AUD/USD", "AUD/JPY", "AUD/CAD", "AUD/NZD", "AUD/GBP", "AUD/EUR", "AUD/CHF"],
    "CAD": ["CAD/USD", "CAD/EUR", "CAD/GBP", "CAD/JPY", "CAD/AUD", "CAD/CHF", "CAD/NZD"],
    "CHF": ["CHF/USD", "CHF/EUR", "CHF/GBP", "CHF/JPY", "CHF/AUD", "CHF/CAD", "CHF/NZD"],
    "NZD": ["NZD/USD", "NZD/EUR", "NZD/GBP", "NZD/JPY", "NZD/AUD", "NZD/CAD", "NZD/CHF"],
    "CNY": ["CNY/USD", "CNY/EUR", "CNY/GBP", "CNY/JPY", "CNY/AUD", "CNY/CAD", "CNY/CHF"]
}

# ---------- DUKASCOPY HELPERS -------------------------------------
def geneva_to_unix(geneva_dt: dt.datetime) -> int:
    # Replace timezone-naive datetime with Geneva timezone
    if geneva_dt.tzinfo is None:
        geneva_dt = geneva_dt.replace(tzinfo=DUKASCOPY_TZ)
    return int(geneva_dt.astimezone(dt.timezone.utc).timestamp() * 1000)

def fetch_bi5(pair: str, year: int, month: int, day: int, hour: int) -> pd.DataFrame:
    url = (
        f"https://datafeed.dukascopy.com/datafeed/{pair.upper()}/"
        f"{year:04d}/{month-1:02d}/{day:02d}/{hour:02d}h_ticks.bi5"
    )
    resp = requests.get(url, timeout=30)
    if resp.status_code != 200:
        return pd.DataFrame()
    
    if not LZ4_AVAILABLE:
        return pd.DataFrame()
    
    raw = lz4.frame.decompress(resp.content)
    data = struct.unpack(f">{len(raw)//4}i", raw)
    cols = ["time", "bid", "ask", "vol", "flag"]
    df = pd.DataFrame([data[i : i + 5] for i in range(0, len(data), 5)], columns=cols)
    df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
    df[["bid", "ask"]] /= 1e5
    return df[["time", "bid", "ask", "vol"]]

# ---------- CORE WORKER ------------------------------------------
def analyse_event(event_row: Dict) -> List[Dict]:
    """
    For one CSV row, download 1-s ticks for all relevant pairs
    and return a list of reaction dicts.
    """
    currency = event_row["currency"]
    if pd.isna(currency) or currency not in PAIR_MAP:
            return []
    
    # parse UTC event time → Zurich
    event_utc = pd.to_datetime(event_row["datetime"], utc=True)
    event_zurich = event_utc.astimezone(DUKASCOPY_TZ)

    start_zurich = event_zurich - dt.timedelta(minutes=10)
    end_zurich = event_zurich + dt.timedelta(minutes=60)  # 1 hour after

    results = []
    for pair in PAIR_MAP[currency]:
        if not pair:  # Skip empty pairs
                continue
        pair_clean = pair.replace("/", "").upper()

        # collect hourly files
        ticks = []
        current = start_zurich.replace(minute=0, second=0, microsecond=0)
        while current <= end_zurich:
            df = fetch_bi5(pair_clean, current.year, current.month, current.day, current.hour)
            if not df.empty:
                ticks.append(df)
            current += dt.timedelta(hours=1)

        if not ticks:
                continue
        
        df = pd.concat(ticks, ignore_index=True)
        # Convert Geneva times to UTC datetime for comparison with tick timestamps
        start_utc = start_zurich.astimezone(dt.timezone.utc)
        end_utc = end_zurich.astimezone(dt.timezone.utc)
        df = df[(df.time >= start_utc) & (df.time <= end_utc)]
        if df.empty:
                continue
            
        # 1-second OHLC
        df["mid"] = (df.bid + df.ask) / 2
        df.set_index("time", inplace=True)
        ohlc = df["mid"].resample("1s").ohlc()
        vol = df["vol"].resample("1s").sum()
        df_1s = pd.concat([ohlc, vol], axis=1).dropna()

        # before/after metrics
        price_before = float(df_1s.iloc[0]["close"])
        price_after = float(df_1s.iloc[-1]["close"])
        change_pips = price_after - price_before
        change_pct = (change_pips / price_before) * 100
        high = float(df_1s["high"].max())
        low = float(df_1s["low"].min())
        volatility = ((high - low) / price_before) * 100

        results.append(
            {
                "event_id": event_row["id"],  # ← Cross-reference with CSV id column
                "event_datetime_utc": event_utc,
                "event_datetime_zurich": event_zurich,
                "currency": currency,
                "event": event_row["event"],
                "impact": event_row["impact"],
                "actual": event_row.get("actual", None),  # From CSV
                "forecast": event_row.get("forecast", None),  # From CSV
                "previous": event_row.get("previous", None),  # From CSV
                "pair": pair,
                "price_before": price_before,
                "price_after": price_after,
                "change_pips": change_pips,
                "change_percent": change_pct,
                "high_during_event": high,
                "low_during_event": low,
                "volatility_percent": volatility,
                "ticks_downloaded": len(df),
            }
        )
    return results

# ---------- MAIN -------------------------------------------------
def main():
    print("\n" + "="*60)
    print("  NEWSBOT - DUKASCOPY DATA COLLECTOR")
    print("="*60 + "\n")
    
    if not os.path.isfile(CSV_FILE):
        print(f"ERROR: {CSV_FILE} not found")
        print(f"Please make sure the file exists in this directory.")
        return
    
    df_csv = pd.read_csv(CSV_FILE)
    df_csv["datetime"] = pd.to_datetime(df_csv["datetime"], utc=True)
    
    # Filter to 2020 onwards only
    cutoff_date = pd.to_datetime("2020-01-01", utc=True)
    df_csv = df_csv[df_csv["datetime"] >= cutoff_date]
    
    print(f"Found {len(df_csv)} events to process (2020 onwards)")
    print(f"Collecting 1-second tick data from Dukascopy...\n")

    all_reactions = []
    for _, row in tqdm(df_csv.iterrows(), total=len(df_csv), desc="Events"):
        reactions = analyse_event(row)
        all_reactions.extend(reactions)
        time.sleep(0.25)

    # ---- JSON OUTPUT -------------------------------------------------
    import json
    OUTPUT_JSON = "dukascopy_all_reactions.json"
    
    # Always save, even if empty (so you don't lose work!)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_reactions, f, indent=2, default=str)
    
    if not all_reactions:
        print(f"\n⚠ No reactions collected")
        print(f"File saved (empty): {OUTPUT_JSON}")
        print("This could mean:")
        print("  - Events are too old (Dukascopy only has recent data)")
        print("  - Events on weekends (markets closed)")
        print("  - Currency pairs not available")
        return
    
    print(f"\n✅ Saved {len(all_reactions)} reactions → {OUTPUT_JSON}")
    print(f"Total pairs analyzed: {len(all_reactions)}")
    print("\n" + "="*60)
    print("  Done!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
