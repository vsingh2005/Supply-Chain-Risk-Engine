# Supply Chain Risk & Inventory Optimization Engine

A quantitative operations analytics and stochastic simulation suite designed for multi-echelon supply chain networks under demand volatility, supplier disruption risks, and capacity constraints.

## Overview & Methodology

```
[ Stochastic Demand Models ] ──┐
 (Geometric Brownian / Poisson) ├─► [ Monte Carlo Simulation ] ──► [ Mixed-Integer Linear Program ]
[ Supplier Disruption Rates ]  ──┘    (Value at Risk / CVaR)         (PuLP / Cost Optimization)
```

## Features
- **Stochastic Demand Forecasting**: Geometric Brownian Motion, Poisson arrival processes, and seasonal Holt-Winters simulation.
- **Vulnerability & Disruption Scoring**: Value at Risk (VaR), Conditional Value at Risk (CVaR), and network bottleneck centrality.
- **Multi-Echelon Inventory Optimization**: Mixed-Integer Linear Programming (MILP) solving safety stock levels, holding costs, and stockout penalties.
- **Scenario Sensitivity Analysis**: Stress testing lead times and geopolitical supplier disruption scenarios.

## Tech Stack
- **Language**: Python 3.11+
- **Optimization & Math**: SciPy, NumPy, PuLP, Pandas
- **Testing & Quality**: Pytest, Ruff

## Quickstart

```bash
# Install package
pip install -e .

# Run test suite
pytest tests/ -v
```
