# Implements rule logic (MA, breakout, volume)


import pandas as pd
import logging
import os
from datetime import datetime
from src.signal_rules import apply_all_rules
from src.utils import load_config, find_latest_ohlcv_file, extract_date_from_filename

def generate_signals(config):
    market_code = config.get("market_code", "idx")
    ohlcv_dir = config.get("ohlcv_dir", "data/raw_ohlcv/")
    output_dir = config.get("output_dir", "output/")

    ohlcv_path = find_latest_ohlcv_file(ohlcv_dir, market_code)

    if not ohlcv_path or not os.path.exists(ohlcv_path):
        logging.error(f"OHLCV file not found in {ohlcv_path} for market {market_code}")
        return

    df = pd.read_csv(ohlcv_path, parse_dates=["Date"])
    if df.empty:
        logging.warning("OHLCV file is empty. Skipping signal generation.")
        return

    signals = []

    for ticker in df["Ticker"].unique():
        ticker_df = df[df["Ticker"] == ticker].sort_values("Date").copy()

        result = apply_all_rules(ticker_df)

        if result["passed"]:
            latest_close = ticker_df.iloc[-1]["Close"]
            signals.append({
                "Market": ticker_df.iloc[-1]["Market"],
                "Ticker": ticker,
                "Close": latest_close,
                "Signal_Reasons": ", ".join(result["reasons"])
            })
    
    os.makedirs(output_dir, exist_ok=True)

    filename = f"signals_{extract_date_from_filename(ohlcv_path)}.csv"
    output_file = os.path.join(output_dir, filename)

    if not signals:
        logging.info("No tickers passed all signal filters.")
        # Write empty file with header
        with open(output_file, "w") as f:
            f.write("Market,Ticker,Close,Signal_Reasons\n")
        logging.info(f"Empty signal file written to {output_file}")
        return

    signals_df = pd.DataFrame(signals)
    signals_df.to_csv(output_file, index=False)
    logging.info(f"Generated signals CSV: {output_file}")