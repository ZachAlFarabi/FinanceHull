# src/ingest.py
# The purpose of this script is to download the adjusted prices and store as SQL db

import yfinance as yf
import pandas as pd
from db import get_connection, init_db

DB_PATH = "data/market_data.db"

TICKERS = {
    "SP500": "^GSPC",
    "NASDAQ": "^NDX",
    "RUSSELL": "^RUT",
    "ASX200": "^AXJO",
    "TREASURY": "IEF",
    "HY_CREDIT": "HYG",
    "GOLD": "GLD",
    "VIX": "^VIX"
}

START = "2000-01-01"


def main():
    init_db()
    conn = get_connection()

    data = yf.download(TICKERS, start=START, auto_adjust=True)["Close"]

    records = []
    for date, row in data.iterrows():
        for ticker in TICKERS:
            if pd.notna(row[ticker]):
                records.append((date.strftime("%Y-%m-%d"), ticker, float(row[ticker])))

    conn.executemany(
        "INSERT OR REPLACE INTO prices VALUES (?, ?, ?)",
        records
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()