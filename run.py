# run.py

from src import data_fetcher, generate_signals, utils
from datetime import datetime
import logging
import os

def setup_logging(config):
    log_dir = config.get("log_dir", "logs/")
    mode = config.get("mode", "prod")
    date_str = datetime.now().strftime("%Y%m%d")

    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    info_handler = logging.FileHandler(os.path.join(log_dir, f"{mode}_info_{date_str}.log"))
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    error_handler = logging.FileHandler(os.path.join(log_dir, f"{mode}_error_{date_str}.log"))
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers = []
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

def main():
    config = data_fetcher.load_config()
    utils.ensure_directories(config)
    setup_logging(config)

    logging.info("Starting IndoTrader signal ingestion process...")

    tickers = data_fetcher.load_tickers()
    logging.info(f"Loaded {len(tickers)} tickers.")

    df = data_fetcher.fetch_all_ohlcv(tickers, config)
    if df.empty:
        logging.warning("No OHLCV data was fetched.")
        return

    data_fetcher.save_ohlcv_to_file(df, config)
    logging.info("Raw OHLCV data saved.")

    generate_signals.generate_signals(config)
    logging.info("Signal generation completed.")

if __name__ == "__main__":
    main()