import pandas as pd
from src.signal_rules import apply_all_rules

def test_signal_rules_match():
    # Mock DataFrame with conditions that should all pass
    data = {
        "Date": pd.date_range(end="2025-07-05", periods=50),
        "Close": [100] * 49 + [120],  # Close > MA50 & 20-day high
        "High": [100] * 49 + [120],   # Sets new high
        "Volume": [500] * 49 + [1000]  # Volume > avg
    }
    df = pd.DataFrame(data)
    result = apply_all_rules(df)

    assert result["passed"] == True
    assert set(result["reasons"]) == {"ma_50", "breakout_20", "volume_spike_20"}

def test_signal_rules_fail():
    # All values flat, nothing breaks out
    data = {
        "Date": pd.date_range(end="2025-07-05", periods=50),
        "Close": [100] * 50,
        "High": [100] * 50,
        "Volume": [100] * 50
    }
    df = pd.DataFrame(data)
    result = apply_all_rules(df)

    assert result["passed"] == False
    assert len(result["partial_matches"]) == 0