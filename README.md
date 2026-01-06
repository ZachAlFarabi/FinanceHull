# FinanceHull

A quantitative research pipeline for financial time series analysis combining  
stochastic differential equations, rolling multivariate statistics, clustering,  
and convex hull geometry for regime detection and market structure analysis.

---

## Project Overview

This project studies financial markets through a **geometric and stochastic lens**:
- Market states are modeled as multivariate stochastic processes
- Rolling windows define evolving high-dimensional point clouds
- Convex hulls capture feasible return regimes and boundary behavior
- Hull dynamics are later linked to SDEs, clustering, and regime shifts

The emphasis is on **theory-driven, data-heavy, reproducible research**.

---

## Repository Structure

src/
  config.py        # Ticker configuration and constants
  db.py            # SQLite schema and connection helpers
  ingest.py        # Market data acquisition (yfinance → SQLite)
  preprocess.py    # Cleaning, alignment, log-returns
  rolling.py       # Rolling multivariate statistics
  visProt1.py      # HTML report & visual diagnostics
  pipe.py          # Orchestrates full pipeline

data/
  finance_hull.db  # SQLite database (generated, ignored by git)

reports/
  mean_summary.html  # Rolling statistics summary report
  prices_1y.png      # Past-year price plot
  prices_1y.csv      # Past-year price data

requirements.txt     # Reproducible environment
README.md

---

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Running and Viewing 

Run the following:
``` bash
python3 ./src/pipe.py
open reports/mean_summary.html
```