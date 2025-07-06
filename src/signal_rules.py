# Full signal pipeline

import pandas as pd

def ma_50_rule(df: pd.DataFrame) -> pd.Series:
    """
    Close > 50-day moving average
    """
    ma50 = df["Close"].rolling(window=50).mean()
    return df["Close"] > ma50

def breakout_20_rule(df: pd.DataFrame) -> pd.Series:
    """
    Close >= 20-day high (breakout)
    """
    high_20 = df["High"].rolling(window=20).max()
    return df["Close"] >= high_20

def volume_spike_20_rule(df: pd.DataFrame) -> pd.Series:
    """
    Volume > 20-day average volume
    """
    avg_vol = df["Volume"].rolling(window=20).mean()
    return df["Volume"] > avg_vol

def apply_all_rules(df: pd.DataFrame) -> dict:
    """
    Apply all rules to the last row of a ticker's dataframe.
    Return dict with matched results.
    """
    if len(df) < 50:
        return {"passed": False, "reasons": [], "partial_matches": []}

    result = {
        "ma_50": ma_50_rule(df).iloc[-1],
        # "breakout_20": breakout_20_rule(df).iloc[-1],
        # "volume_spike_20": volume_spike_20_rule(df).iloc[-1],
    }

    # Full AND match
    passed = all(result.values())

    # Partial match list
    partials = [rule for rule, passed in result.items() if passed]

    return {
        "passed": passed,
        "reasons": partials if passed else [],
        "partial_matches": partials,
    }