# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
cd C:\Dev\claude\stock-dashboard
python -m streamlit run app.py --browser.gatherUsageStats false --server.headless true
```

> Use `python -m streamlit` instead of `streamlit` directly — the `streamlit` binary may not be on PATH.

The app runs at `http://localhost:8501`.

## Architecture

Two-file separation of concerns:

- **`data.py`** — all data fetching and computation. `fetch_data()` downloads OHLCV data from Yahoo Finance via yfinance for each ticker. `calc_performance()` normalizes close prices to % return from the first trading day of 2025. `df.columns.get_level_values(0)` is required to flatten the MultiIndex yfinance returns when downloading a single ticker.

- **`app.py`** — pure presentation layer. Calls `load_data()` (a cached wrapper around `fetch_data()` with 1h TTL) then renders: metric cards → closing price chart → cumulative performance chart → weekly volume bar chart. All charts use `plotly.graph_objects` with `go.Scatter` / `go.Bar`; no Plotly Express.

## Key Details

- Tickers are B3 stocks with the `.SA` suffix required by Yahoo Finance: `SANB11.SA`, `ITUB4.SA`, `VALE3.SA`.
- `START = "2025-01-01"` in `data.py` is the fixed start date for all data.
- Brand colors per stock are defined in `COLORS` in `app.py` and must be kept in sync if tickers change.
- To add a new stock: add it to `TICKERS` in `data.py` and add its brand color to `COLORS` in `app.py`.
