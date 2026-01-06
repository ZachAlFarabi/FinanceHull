import pandas as pd
import sqlite3

conn = sqlite3.connect("data/finance_hull.db")
from src.config import TICKERS

# Example: Rolling stats summary
rolling = pd.read_sql("SELECT * FROM rolling_stats", conn)
# Deserialize mean vectors
import pickle, numpy as np
rolling['mean_vector'] = rolling['mean_vector'].apply(lambda x: np.array(pickle.loads(x)))
rolling['cov_matrix'] = rolling['cov_matrix'].apply(lambda x: np.array(pickle.loads(x)))

# Create a DataFrame of mean returns per ticker (shortened)
mean_df = pd.DataFrame(rolling['mean_vector'].to_list(), columns=list(TICKERS.keys()))
mean_df_summary = mean_df.describe().T  # transpose for pivot-like view

# Color code
styled = mean_df_summary.style.background_gradient(cmap='RdYlGn', axis=1)
styled.to_html("reports/mean_summary.html")  # save HTML file

print("Saved HTML report to reports/mean_summary.html")
