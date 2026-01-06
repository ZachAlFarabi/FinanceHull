# src/preprocess.py
# The purpose of this script is to compute log-returns for further processing

import pandas as pd
import numpy as np
from db import get_connection, init_db

def main():
    init_db()
    conn = get_connection()

    prices = pd.read_sql(
        "SELECT * FROM prices",
        conn,
        parse_dates=["date"]
    ).sort_values(["ticker", "date"])

    # Fixed log-return calculation
    prices["log_return"] = prices.groupby("ticker")["adj_close"].transform(lambda x: np.log(x / x.shift(1)))

    prices = prices.dropna(subset=["log_return"])

    records = [
        (row.date.strftime("%Y-%m-%d"), row.ticker, float(row.log_return))
        for row in prices.itertuples()
    ]

    conn.executemany(
        "INSERT OR REPLACE INTO returns VALUES (?, ?, ?)",
        records
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()