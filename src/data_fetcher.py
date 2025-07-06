# Retrieves OHLCV data from yfinance

import os
import json
import logging
import pandas as pd
import yfinance as yf
from tqdm import tqdm
from datetime import datetime
import yaml

def load_config():
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # If in test mode, merge with test overrides
    if config.get("mode") == "test":
        with open("config/config_test.yaml", "r") as f:
            test_overrides = yaml.safe_load(f)
        config.update(test_overrides)
    return config

def load_tickers(path="data/tickers.json"):
    with open(path, "r") as f:
        return json.load(f)

def fetch_all_ohlcv(tickers, config):
    period = f"{config.get('ohlcv_days', 100)}d"
    market_code = config.get("market_code", "idx")

    all_data = []
    for ticker in tqdm(tickers, desc="Fetching OHLCV"):
        try:
            df = yf.download(
                ticker,
                period=period,
                interval="1d",
                progress=False,
                threads=False,
                auto_adjust=True,
            )

            if df.empty:
                raise ValueError("No data returned")
                
            df = df.reset_index()
            df.columns = df.columns.droplevel(level=1)
            df["Ticker"] = ticker
            df["Market"] = market_code.upper()
            all_data.append(df)

        except Exception as e:
            logging.error(f"Failed to fetch {ticker}: {e}")

    if not all_data:
        return pd.DataFrame()

    combined = pd.concat(all_data, axis=0).reset_index(drop=True)
    return combined[["Market", "Ticker", "Date", "Open", "High", "Low", "Close", "Volume"]]

def save_ohlcv_to_file(df, config):
    if df.empty:
        logging.warning("No OHLCV data to save.")
        return

    market = config["market_code"]
    date_str = df["Date"].max().strftime("%Y%m%d")
    filename = f"{market}-ohlcv-eod-{date_str}.csv"

    full_path = os.path.join(config["ohlcv_dir"], filename)
    df.to_csv(full_path, index=False)
    logging.info(f"Saved OHLCV to {full_path}")