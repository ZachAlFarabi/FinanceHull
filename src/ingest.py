# src/ingest.py
# The purpose of this script is to download the adjusted prices and store as SQL db

import yfinance as yf
import pandas as pd
from db import get_connection, init_db
from .config import TICKERS

DB_PATH = "data/market_data.db"

START = "2015-01-01"

def main():
    init_db()
    conn = get_connection()

    # Extract only the ticker symbols for yfinance
    ticker_list = list(TICKERS.values())

    # Download prices
    data = yf.download(ticker_list, start=START, auto_adjust=True)["Close"]

    # Flatten the DataFrame into rows for SQLite
    records = []
    for date, row in data.iterrows():
        for name, ticker in TICKERS.items():
            if pd.notna(row[ticker]):
                records.append((date.strftime("%Y-%m-%d"), name, float(row[ticker])))

    # Insert into database
    conn.executemany(
        "INSERT OR REPLACE INTO prices VALUES (?, ?, ?)",
        records
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()