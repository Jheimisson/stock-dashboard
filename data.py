import yfinance as yf
import pandas as pd

TICKERS = {
    "Santander": "SANB11.SA",
    "Itaú": "ITUB4.SA",
    "Vale": "VALE3.SA",
}
START = "2025-01-01"


def fetch_data():
    frames = {}
    for name, ticker in TICKERS.items():
        df = yf.download(ticker, start=START, auto_adjust=True, progress=False)
        df.columns = df.columns.get_level_values(0)
        frames[name] = df
    return frames


def calc_performance(frames):
    perf = {}
    for name, df in frames.items():
        close = df["Close"].dropna()
        if len(close) > 0:
            perf[name] = (close / close.iloc[0] - 1) * 100
    return perf
