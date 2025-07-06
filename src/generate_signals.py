# Implements rule logic (MA, breakout, volume)


import pandas as pd
import logging
import os
from datetime import datetime
from signal_rules import apply_all_rules
from utils import load_config

def generate_signals(config):
    market_code = config.get("market_code", "idx")
    ohlcv_dir = config.get("ohlcv_dir", "data/raw_ohlcv/")
    output_dir = config.get("output_dir", "output/")

    # Find latest OHLCV file
    today_str = datetime.today().strftime("%Y%m%d")
    ohlcv_filename = f"{market_code}-ohlcv-eod-{today_str}.csv"
    ohlcv_path = os.path.join(ohlcv_dir, ohlcv_filename)

    if not os.path.exists(ohlcv_path):
        logging.error(f"OHLCV file not found: {ohlcv_path}")
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

    if not signals:
        logging.info("No tickers passed all signal filters.")
        return

    signals_df = pd.DataFrame(signals)
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"signals_{today_str}.csv")
    signals_df.to_csv(output_file, index=False)
    logging.info(f"Generated signals CSV: {output_file}")