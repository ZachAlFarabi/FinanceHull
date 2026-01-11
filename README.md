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
  config.py        # Ticker configuration and constants __
  db.py            # SQLite schema and connection helpers __
  ingest.py        # Market data acquisition __
  preprocess.py    # Cleaning, alignment, log-returns __
  rolling.py       # Rolling multivariate statistics __
  visProt1.py      # HTML report & visual diagnostics __
  pipe.py          # Orchestrates full pipeline __

data/
  finance_hull.db  # SQLite database __

requirements.txt   # Reproducible environment __
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
