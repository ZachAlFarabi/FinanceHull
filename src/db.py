import sqlite3
from pathlib import Path

DB_PATH = Path("data/finance_hull.db")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            date TEXT NOT NULL,
            ticker TEXT NOT NULL,
            adj_close REAL NOT NULL,
            PRIMARY KEY (date, ticker)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS returns (
            date TEXT NOT NULL,
            ticker TEXT NOT NULL,
            log_return REAL NOT NULL,
            PRIMARY KEY (date, ticker)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rolling_stats (
            window_end TEXT NOT NULL,
            window_size INTEGER NOT NULL,
            mean_vector BLOB NOT NULL,
            cov_matrix BLOB NOT NULL,
            PRIMARY KEY (window_end, window_size)
        );
    """)

    conn.commit()
    conn.close()
