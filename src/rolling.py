import pandas as pd
import numpy as np
import pickle
from .db import get_connection, init_db
from .config import TICKERS

WINDOW = 60  # trading days

def main():
    init_db()
    conn = get_connection()

    returns = pd.read_sql(
        "SELECT * FROM returns",
        conn,
        parse_dates=["date"]
    )

    pivot = returns.pivot(index="date", columns="ticker", values="log_return")
    pivot = pivot.dropna()

    dates = pivot.index

    records = []

    for i in range(WINDOW - 1, len(pivot)):
        window_data = pivot.iloc[i - WINDOW + 1 : i + 1].values

        mean_vec = window_data.mean(axis=0)
        cov_mat = np.cov(window_data, rowvar=False)

        records.append((
            dates[i].strftime("%Y-%m-%d"),
            WINDOW,
            pickle.dumps(mean_vec),
            pickle.dumps(cov_mat)
        ))

    conn.executemany(
        "INSERT OR REPLACE INTO rolling_stats VALUES (?, ?, ?, ?)",
        records
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
