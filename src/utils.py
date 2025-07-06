import os, yaml, json, glob, re

def ensure_directories(config: dict):
    """
    Ensure that necessary folders exist before running the pipeline.
    """
    dirs_to_check = [
        config.get("output_dir", "output/"),
        config.get("ohlcv_dir", "data/raw_ohlcv/"),
        config.get("log_dir", "logs/"),
        "data",
        "config",
        "src"
    ]

    for directory in dirs_to_check:
        os.makedirs(directory, exist_ok=True)

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

def find_latest_ohlcv_file(ohlcv_dir, market_code):
    pattern = f"{market_code}-ohlcv-eod-*.csv"
    files = glob.glob(os.path.join(ohlcv_dir, pattern))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def extract_date_from_filename(filepath):
    # e.g. "test_idx-ohlcv-eod-20250704.csv" ➝ "20250704"
    basename = os.path.basename(filepath)
    match = re.search(r"(\d{8})", basename)
    return match.group(1) if match else None