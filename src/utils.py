import os

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