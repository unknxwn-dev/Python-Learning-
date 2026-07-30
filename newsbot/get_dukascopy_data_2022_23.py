"""
Simple Dukascopy Data Collector - 2022-2023
- Reads ForexScrape.CSV
- Gets 1-second tick data from Dukascopy
- Outputs clean JSON for AI training
- Date Range: 2022-01-01 to 2023-12-31
"""

import sys
import datetime as dt

# Try to import lz4 - if it fails, we'll handle it in the function
try:
    import lz4.frame
    LZ4_AVAILABLE = True
except ImportError:
    LZ4_AVAILABLE = False
    print("Warning: lz4 not available - decompression will be skipped")

import pandas as pd
import requests
import struct
import os
import time
import json
from tqdm import tqdm

# ---------- CONFIG -------------------------------------------------
DUKASCOPY_TZ = dt.timezone(dt.timedelta(hours=2))  # Zurich/Geneva time
CSV_FILE = "ForexScrape.CSV"
OUTPUT_JSON = "training_data_2022_23.json"

# Date range for this script
START_DATE = "2022-01-01"
END_DATE = "2023-12-31"

# Pairs to check for each currency
PAIR_MAP = {
    "USD": ["USDEUR", "USDGBP", "USDJPY", "USDCHF", "USDCAD", "USDAUD", "USDCHF"],
    "EUR": ["EURUSD", "EURGBP", "EURJPY", "EURCHF", "EURCAD", "EURAUD", "EURNZD"],
    "GBP": ["GBPUSD", "GBPEUR", "GBPJPY", "GBPCHF", "GBPCAD", "GBPAUD", "GBPNZD"],
    "JPY": ["JPYUSD", "JPYEUR", "JPYGBP", "JPYAUD", "JPYCAD", "JPYNZD", "JPYCHF"],
    "AUD": ["AUDUSD", "AUDEUR", "AUDGBP", "AUDJPY", "AUDCAD", "AUDNZD", "AUDCHF"],
    "CAD": ["CADUSD", "CADEUR", "CADGBP", "CADJPY", "CADAUD", "CADNZD", "CADCHF"],
    "CHF": ["CHFUSD", "CHFEUR", "CHFGBP", "CHFJPY", "CHFAUD", "CHFCAD", "CHFNZD"],
    "NZD": ["NZDUSD", "NZDEUR", "NZDGBP", "NZDJPY", "NZDAUD", "NZDCAD", "NZDCHF"],
    "CNY": ["CNYUSD", "CNYEUR", "CNYGBP", "CNYJPY", "CNYAUD", "CNYCAD", "CNYCHF"]
}

# ---------- FUNCTIONS ----------------------------------------------
def fetch_dukascopy_hour(pair: str, year: int, month: int, day: int, hour: int):
    """Download one hour of tick data from Dukascopy"""
    url = f"https://datafeed.dukascopy.com/datafeed/{pair}/{year:04d}/{month-1:02d}/{day:02d}/{hour:02d}h_ticks.bi5"
    
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code != 200:
            return pd.DataFrame()
        
        # Check if lz4 is available
        if not LZ4_AVAILABLE:
            print(f"  Skipping {pair} - lz4 not available for decompression")
            return pd.DataFrame()
        
        # Decompress LZ4 data
        raw = lz4.frame.decompress(resp.content)
        data = struct.unpack(f">{len(raw)//4}i", raw)
        
        # Parse into DataFrame
        rows = [data[i:i+5] for i in range(0, len(data), 5)]
        df = pd.DataFrame(rows, columns=["time", "bid", "ask", "vol", "flag"])
        
        # Convert timestamps and prices
        df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
        df["bid"] = df["bid"] / 1e5
        df["ask"] = df["ask"] / 1e5
        
        return df[["time", "bid", "ask", "vol"]]
    
    except Exception as e:
        return pd.DataFrame()


def get_price_snapshot(pair: str, target_time: dt.datetime) -> float:
    """Get price at a specific time (snapshot)"""
    try:
        target_utc = target_time.astimezone(dt.timezone.utc)
        hour_time = target_utc.replace(minute=0, second=0, microsecond=0)
        
        df = fetch_dukascopy_hour(
            pair,
            hour_time.year,
            hour_time.month,
            hour_time.day,
            hour_time.hour
        )
        
        if df.empty:
            return None
        
        # Find closest tick to target time
        df["time"] = pd.to_datetime(df["time"], utc=True)
        df = df[(df["time"] >= target_utc - dt.timedelta(minutes=5)) & 
                (df["time"] <= target_utc + dt.timedelta(minutes=5))]
        
        if df.empty:
            return None
        
        # Get mid price
        df["mid"] = (df["bid"] + df["ask"]) / 2
        return float(df["mid"].iloc[len(df)//2])  # Middle price
        
    except Exception:
        return None


def get_event_data(event_id, event_datetime, currency, event_name, impact, 
                   minutes_before=10, minutes_after=60, 
                   actual=None, forecast=None, previous=None):
    """
    Get comprehensive price data:
    - 1-second data: 10 min before → 1 hour after
    - Snapshot: 1 hour before event
    - Snapshot: 1 day before event
    - Hourly snapshots: Every hour for 24 hours after
    """
    
    if pd.isna(currency) or currency not in PAIR_MAP:
        return []
    
    # Convert to Zurich time
    event_utc = pd.to_datetime(event_datetime, utc=True)
    event_zurich = event_utc.astimezone(DUKASCOPY_TZ)
    
    # Time points to capture
    one_hour_before = event_zurich - dt.timedelta(hours=1)
    one_day_before = event_zurich - dt.timedelta(days=1)
    one_day_after = event_zurich + dt.timedelta(days=1)
    
    # Short-term window (1-second data)
    start_time = event_zurich - dt.timedelta(minutes=minutes_before)
    end_time = event_zurich + dt.timedelta(minutes=minutes_after)
    
    results = []
    
    # Process each pair for this currency
    for pair in PAIR_MAP[currency]:
        if not pair:
            continue
        
        pair_clean = pair.replace("/", "").upper()
        
        # ===== 1. GET SHORT-TERM 1-SECOND DATA (10 min before → 1 hour after) =====
        all_ticks = []
        current_hour = start_time.replace(minute=0, second=0, microsecond=0)
        
        while current_hour <= end_time:
            df = fetch_dukascopy_hour(
                pair_clean,
                current_hour.year,
                current_hour.month,
                current_hour.day,
                current_hour.hour
            )
            if not df.empty:
                all_ticks.append(df)
            current_hour += dt.timedelta(hours=1)
        
        # Process short-term data
        short_term_data = {}
        if all_ticks:
            df = pd.concat(all_ticks, ignore_index=True)
            start_utc = start_time.astimezone(dt.timezone.utc)
            end_utc = end_time.astimezone(dt.timezone.utc)
            df = df[(df["time"] >= start_utc) & (df["time"] <= end_utc)]
            
            if not df.empty:
                df["mid"] = (df["bid"] + df["ask"]) / 2
                df.set_index("time", inplace=True)
                
                ohlc = df["mid"].resample("1S").ohlc()
                volume = df["vol"].resample("1S").sum()
                bars = pd.concat([ohlc, volume], axis=1).dropna()
                
                if not bars.empty:
                    short_term_data = {
                        "price_before": float(bars.iloc[0]["close"]),
                        "price_after": float(bars.iloc[-1]["close"]),
                        "price_high": float(bars["high"].max()),
                        "price_low": float(bars["low"].min()),
                        "num_ticks": len(df),
                        "num_1s_bars": len(bars),
                        "price_1s_data": bars.head(100).reset_index().to_dict('records') if len(bars) > 0 else []  # Store first 100 seconds
                    }
        
        # ===== 2. GET PRICE SNAPSHOTS =====
        price_1h_before = get_price_snapshot(pair_clean, one_hour_before)
        price_1d_before = get_price_snapshot(pair_clean, one_day_before)
        price_at_event = get_price_snapshot(pair_clean, event_zurich)
        
        # ===== 3. GET HOURLY SNAPSHOTS FOR 24 HOURS AFTER =====
        hourly_prices = []
        current_hour_check = event_zurich.replace(minute=0, second=0, microsecond=0)
        
        while current_hour_check <= one_day_after:
            hour_price = get_price_snapshot(pair_clean, current_hour_check)
            if hour_price is not None:
                hourly_prices.append({
                    "hour_offset": (current_hour_check - event_zurich).total_seconds() / 3600,
                    "datetime": str(current_hour_check.astimezone(dt.timezone.utc)),
                    "price": round(hour_price, 5)
                })
            current_hour_check += dt.timedelta(hours=1)
        
        # Skip if no data collected
        if not short_term_data and not hourly_prices and price_at_event is None:
            continue
        
        # Calculate changes
        base_price = short_term_data.get("price_before") if short_term_data else price_at_event
        
        if base_price is None:
            continue
        
        # Short-term change (immediate reaction)
        short_change_pct = 0.0
        short_volatility = 0.0
        if short_term_data:
            short_change = short_term_data["price_after"] - short_term_data["price_before"]
            short_change_pct = (short_change / short_term_data["price_before"]) * 100
            short_volatility = ((short_term_data["price_high"] - short_term_data["price_low"]) / 
                               short_term_data["price_before"]) * 100
        
        # Long-term changes
        price_1h_after = None
        price_24h_after = None
        
        if hourly_prices:
            # Price 1 hour after
            hour_1_after = next((h for h in hourly_prices if h["hour_offset"] >= 1), None)
            if hour_1_after:
                price_1h_after = hour_1_after["price"]
            
            # Price 24 hours after
            hour_24_after = next((h for h in hourly_prices if h["hour_offset"] >= 24), None)
            if hour_24_after:
                price_24h_after = hour_24_after["price"]
        
        # Calculate long-term changes
        change_1h_after_pct = None
        change_24h_after_pct = None
        
        if price_1h_after is not None:
            change_1h_after_pct = ((price_1h_after - base_price) / base_price) * 100
        
        if price_24h_after is not None:
            change_24h_after_pct = ((price_24h_after - base_price) / base_price) * 100
        
        # Build result
        result = {
            "event_id": event_id,
            "event_datetime_utc": str(event_utc),
            "currency": currency,
            "event_name": event_name,
            "impact": impact,
            "actual": actual,
            "forecast": forecast,
            "previous": previous,
            "pair": pair,
            
            # Short-term (10 min before → 1 hour after, 1-second data)
            "short_term": {
                "price_before": round(short_term_data.get("price_before", base_price), 5),
                "price_after": round(short_term_data.get("price_after", base_price), 5),
                "price_high": round(short_term_data.get("price_high", base_price), 5),
                "price_low": round(short_term_data.get("price_low", base_price), 5),
                "change_percent": round(short_change_pct, 4),
                "volatility_percent": round(short_volatility, 4),
                "num_1s_bars": short_term_data.get("num_1s_bars", 0)
            },
            
            # Historical snapshots
            "price_1h_before": round(price_1h_before, 5) if price_1h_before else None,
            "price_1d_before": round(price_1d_before, 5) if price_1d_before else None,
            "price_at_event": round(price_at_event, 5) if price_at_event else round(base_price, 5),
            
            # Long-term (hourly snapshots for 24 hours)
            "long_term": {
                "hourly_prices": hourly_prices,
                "price_1h_after": round(price_1h_after, 5) if price_1h_after else None,
                "price_24h_after": round(price_24h_after, 5) if price_24h_after else None,
                "change_1h_after_pct": round(change_1h_after_pct, 4) if change_1h_after_pct is not None else None,
                "change_24h_after_pct": round(change_24h_after_pct, 4) if change_24h_after_pct is not None else None,
                "num_hourly_snapshots": len(hourly_prices)
            }
        }
        
        results.append(result)
    
    return results


# ---------- MAIN ---------------------------------------------------
def main():
    print("\n" + "="*60)
    print("  DUKASCOPY DATA COLLECTOR - 2022-2023")
    print("  Comprehensive Price Data Collection")
    print("="*60)
    print(f"\nDate Range: {START_DATE} to {END_DATE}")
    print("\nCollecting:")
    print("  ✓ 1-second data: 10 min before → 1 hour after")
    print("  ✓ Snapshot: 1 hour before event")
    print("  ✓ Snapshot: 1 day before event")
    print("  ✓ Hourly snapshots: Every hour for 24 hours after")
    print("="*60 + "\n")
    
    # Check CSV exists
    if not os.path.isfile(CSV_FILE):
        print(f"❌ ERROR: {CSV_FILE} not found!")
        print(f"   Place your event CSV in this directory.")
        return
    
    # Load events
    print(f"Loading events from {CSV_FILE}...")
    df_events = pd.read_csv(CSV_FILE)
    
    # Filter to date range
    df_events["datetime"] = pd.to_datetime(df_events["datetime"], utc=True)
    start_date = pd.to_datetime(START_DATE, utc=True)
    end_date = pd.to_datetime(END_DATE, utc=True) + dt.timedelta(days=1)  # Include end date
    df_events = df_events[(df_events["datetime"] >= start_date) & (df_events["datetime"] < end_date)]
    print(f"✓ Filtered to {len(df_events)} events from {START_DATE} to {END_DATE}")
    
    required_cols = ["id", "datetime", "currency", "event", "impact"]
    missing = [col for col in required_cols if col not in df_events.columns]
    if missing:
        print(f"❌ ERROR: Missing columns: {missing}")
        return
    
    print(f"✓ Found {len(df_events)} events\n")
    
    # Process each event
    all_data = []
    
    for idx, row in tqdm(df_events.iterrows(), total=len(df_events), desc="Processing events"):
        event_data = get_event_data(
            event_id=row["id"],
            event_datetime=row["datetime"],
            currency=row["currency"],
            event_name=row["event"],
            impact=row["impact"],
            actual=row.get("actual", None),
            forecast=row.get("forecast", None),
            previous=row.get("previous", None)
        )
        all_data.extend(event_data)
        time.sleep(0.25)  # Be nice to Dukascopy
    
    # Save results - ALWAYS save, even if empty
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)
    
    if not all_data:
        print(f"\n⚠️  No data collected!")
        print(f"   File saved (empty): {OUTPUT_JSON}")
        print("   Check that events are recent and during market hours.")
        return
    
    print(f"\n✅ SUCCESS!")
    print(f"   Collected {len(all_data)} data points")
    print(f"   Saved to: {OUTPUT_JSON}")
    
    # Show summary
    df_results = pd.DataFrame(all_data)
    print(f"\n📊 Summary:")
    print(f"   Events processed: {df_results['event_id'].nunique()}")
    print(f"   Currency pairs: {df_results['pair'].nunique()}")
    print(f"   Avg change: {df_results['short_term'].apply(lambda x: x['change_percent']).mean():.2f}%")
    print(f"   Avg volatility: {df_results['short_term'].apply(lambda x: x['volatility_percent']).mean():.2f}%")
    
    print("\n" + "="*60)
    print("  Ready for AI training!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

