# src/preprocess.py
# The purpose of this script is to compute log-returns for further processing

import sqlite3
import pandas as pd
import numpy as np

DB_PATH = "data/market_data.db"

def compute_log_returns():
    # Conn to db
    conn = sqlite3.connect(DB_PATH)

    # Read price
    prices = pd.read_sql(
        "SELECT date, asset, adj_close FROM prices ORDER BY date",
        conn,
        parse_dates=["date"]
    )

    returns = []

    # Go through assets, sort by date, find log returns to temp
    for asset, g in prices.groupby("asset"):
        g = g.sort_values("date")
        log_ret = np.log(g.adj_close).diff()

        tmp = pd.DataFrame({
            "date": g.date,
            "asset": asset,
            "log_return": log_ret
        })

        returns.append(tmp)

    # Concat and replace
    returns_df = pd.concat(returns).dropna()

    returns_df.to_sql(
        "returns",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()
    print("Computed log-returns and stored in SQLite.")


if __name__ == "__main__":
    compute_log_returns()