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
ingest.py # Market data acquisition (yfinance)
preprocess.py # Cleaning, alignment, log-returns
rolling.py # Rolling multivariate statistics & geometry
pipeline.py # Orchestrates full pipeline

data/ # Generated data (ignored by git)
requirements.txt # Reproducible environment


---

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt