# IndoTrader – Signal Generator MVP

A modular, maintainable system to generate daily EOD trading signals for Indonesian stocks (`.JK`) using configurable technical rules.

## 🎯 Objective

- Fetch daily OHLCV data for a predefined list of IDX tickers
- Apply configurable technical signal rules
- Generate CSV reports:
  - `signals_trading_YYYYMMDD.csv`: stocks that meet **all** rules (execution-worthy)
  - `signals_analysis_YYYYMMDD.csv`: stocks that meet **any** rule (research-worthy)

## 🗂️ Project Structure
```
indo_trader/
├── config/
│ └── config.yaml # Signal parameters (MA window, etc.)
├── data/
│ ├── tickers.json # Static list of .JK tickers
│ └── raw_ohlcv/ # Raw OHLCV snapshot per day
├── logs/
│ ├── error_YYYYMMDD.log # Ticker-level + global errors
│ └── info_YYYYMMDD.log # Optional run summaries
├── output/
│ ├── signals_trading_YYYYMMDD.csv # Stocks passing all rules
│ └── signals_analysis_YYYYMMDD.csv # Stocks passing any rule
├── src/
│ ├── data_fetcher.py # Fetch OHLCV from yfinance
│ ├── signal_rules.py # Signal rule logic
│ ├── generate_signals.py # Pipeline: fetch → filter → output
│ └── utils.py # Helpers (date, I/O, etc.)
├── run.py # CLI entrypoint
└── requirements.txt # Python dependencies
```
---

## 📈 Signal Rules

Configured in `config/config.yaml`, implemented in `src/signal_rules.py`.

### ✅ Default MVP Rules (AND logic for trading signals)
- Price > 50-day Moving Average
- Price >= 20-day High
- Volume > 20-day Average Volume

Signals for analysis are triggered if **any rule matches** (OR logic).

## 🛠️ How to Run
Install dependencies:

```
pip install -r requirements.txt
```

Then generate signals:
```
python run.py
```

This will:
- Load tickers
- Download data from Yahoo Finance
- Apply signal rules
- Output two CSVs
- Log activity and errors

## 🪵 Logging
Logs are stored in logs/:
- error_YYYYMMDD.log: Failed tickers or API issues
- info_YYYYMMDD.log: Success summaries

Format:
```
[2025-07-04 17:30:21] ERROR: Failed to fetch BBCA.JK - HTTPError: 404
[2025-07-04 17:30:25] INFO: Signal generation completed successfully.
```

## 📌 Notes
Ticker list (tickers.json) is manually maintained in MVP.

EOD data is stored per day, not per ticker — optimized for backtesting and reproducibility.

Ready for future enhancements: retry logic, Telegram alerts, LLM integration, backtests, journaling.

## 📍 License
MIT – Use freely with attribution. This is a personal project intended for educational and research purposes.

---
