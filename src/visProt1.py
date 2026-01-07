import pandas as pd
import sqlite3
from .config import TICKERS
from pathlib import Path
import pickle, numpy as np
import matplotlib.pyplot as plt

conn = sqlite3.connect("data/finance_hull.db")

# Rolling stats
rolling = pd.read_sql("SELECT * FROM rolling_stats", conn)

rolling['mean_vector'] = rolling['mean_vector'].apply(
    lambda x: np.array(pickle.loads(x))
)
rolling['cov_matrix'] = rolling['cov_matrix'].apply(
    lambda x: np.array(pickle.loads(x))
)

mean_df = pd.DataFrame(
    rolling['mean_vector'].to_list(),
    columns=list(TICKERS.keys())
)

mean_df_summary = mean_df.describe().T

# COlour function
def color_pos_neg(val):
    if pd.isna(val):
        return ""
    if val > 0:
        return "background-color: rgba(0, 150, 0, 0.45)"
    elif val < 0:
        return "background-color: rgba(200, 0, 0, 0.45)"
    else:
        return "background-color: rgba(200, 200, 200, 0.2)"

# Report directory
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

# Style table
styled = (
    mean_df_summary.style
        .map(color_pos_neg)
        .format("{:.4f}")
        .set_caption(
            "Rolling Mean Returns Summary<br>"
            "<small>Green = Positive, Red = Negative</small>"
        )
)

# Load price
prices = pd.read_sql(
    "SELECT date, ticker, adj_close FROM prices",
    conn,
    parse_dates=["date"]
)

price_pivot = (
    prices
    .pivot(index="date", columns="ticker", values="adj_close")
    .sort_index()
)

price_1y = price_pivot.tail(252)

price_1y.to_csv(REPORT_DIR / "prices_1y.csv")

# Plotting
plt.figure(figsize=(10, 5))

for ticker in price_1y.columns:
    plt.plot(price_1y.index, price_1y[ticker], label=ticker)

plt.yscale("log")
plt.title("Asset Prices - Past 12 Months")
plt.xlabel("Date")
plt.ylabel("Adjusted Close Log Price")
plt.legend()
plt.tight_layout()
plt.savefig(REPORT_DIR / "prices_1y.png")
plt.close()

# Extend html
html_extra = """
<hr>
<button onclick="toggleDetails()">Show / Hide Price Details</button>

<div id="details" style="display:none; margin-top:20px;">
  <h3>Past Year Prices</h3>
  <img src="prices_1y.png" width="900">
  <p>
    Raw data available in <code>prices_1y.csv</code>
  </p>
</div>

<script>
function toggleDetails() {
  var x = document.getElementById("details");
  x.style.display = (x.style.display === "none") ? "block" : "none";
}
</script>
"""

# Write html
with open(REPORT_DIR / "mean_summary.html", "w") as f:
    f.write(styled.to_html())
    f.write(html_extra)

print("Saved HTML report to reports/mean_summary.html")
