# src/rolling.py

import sqlite3
import pandas as pd
import numpy as np

DB_PATH = "data/market_data.db"
WINDOW = 60


def load_returns_matrix():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT date, asset, log_return FROM returns",
        conn,
        parse_dates=["date"]
    )

    conn.close()

    # Pivot to wide format: rows = dates, cols = assets
    R = (
        df
        .pivot(index="date", columns="asset", values="log_return")
        .sort_index()
        .dropna()
    )

    return R


def compute_multivariate_rolling():
    R = load_returns_matrix()
    assets = R.columns.tolist()

    mean_records = []
    cov_records = []
    eig_records = []

    for i in range(WINDOW, len(R)):
        window = R.iloc[i-WINDOW:i]
        t = R.index[i]

        # Mean vector
        mu = window.mean()

        # Covariance matrix
        Sigma = window.cov()

        # Eigen-decomposition
        eigvals = np.linalg.eigvalsh(Sigma)

        # Store mean vector
        for asset in assets:
            mean_records.append({
                "window_end": t,
                "asset": asset,
                "mean": mu[asset]
            })

        # Store covariance (long format)
        for a1 in assets:
            for a2 in assets:
                cov_records.append({
                    "window_end": t,
                    "asset_i": a1,
                    "asset_j": a2,
                    "covariance": Sigma.loc[a1, a2]
                })

        # Store eigenvalues
        for k, val in enumerate(sorted(eigvals, reverse=True)):
            eig_records.append({
                "window_end": t,
                "component": k + 1,
                "eigenvalue": val
            })

    conn = sqlite3.connect(DB_PATH)

    pd.DataFrame(mean_records).to_sql(
        "rolling_means",
        conn,
        if_exists="replace",
        index=False
    )

    pd.DataFrame(cov_records).to_sql(
        "rolling_covariances",
        conn,
        if_exists="replace",
        index=False
    )

    pd.DataFrame(eig_records).to_sql(
        "rolling_eigenvalues",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()
    print(f"Computed multivariate rolling statistics (W={WINDOW}).")


if __name__ == "__main__":
    compute_multivariate_rolling()
