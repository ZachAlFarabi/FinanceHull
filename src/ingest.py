# src/ingest.py
# The purpose of this script is to download the adjusted prices and store as SQL db

import os
import sqlite3
import yfinance as yf
import pandas as pd

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

START_DATE = "2000-01-01"


def ingest_prices():
    # Directory existance
    os.makedirs("data", exist_ok=True)

    # Download index prices
    prices = yf.download(
        list(TICKERS.values()),
        start=START_DATE,
        auto_adjust=True,
        progress=False
    )["Close"]

    # Make keys
    prices.columns = TICKERS.keys()
    prices = prices.dropna(how="all")

    # Asset and long prices
    prices_long = (
        prices
        .reset_index()
        .melt(id_vars="Date", var_name="asset", value_name="adj_close")
        .rename(columns={"Date": "date"})
    )

    # Conn
    conn = sqlite3.connect(DB_PATH)
    prices_long.to_sql(
        "prices",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()
    print("Ingested adjusted prices into SQLite.")


if __name__ == "__main__":
    ingest_prices()