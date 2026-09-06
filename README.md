# Supply-Chain-Risk-Engine

[![CI](https://github.com/vsingh2005/Supply-Chain-Risk-Engine/actions/workflows/ci.yml/badge.svg)](https://github.com/vsingh2005/Supply-Chain-Risk-Engine/actions/workflows/ci.yml)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)

Quantitative operations analytics and stochastic simulation suite for multi-echelon supply chain networks.

## Overview & Methodology

```
[ Stochastic Demand Models ] ──┐
 (Geometric Brownian / Poisson) ├─► [ Monte Carlo Simulation ] ──► [ Mixed-Integer Linear Program ]
[ Supplier Disruption Rates ]  ──┘    (Value at Risk / CVaR)         (PuLP / Cost Optimization)
```

## Features

- **Stochastic Demand Forecasting**: Geometric Brownian Motion, Poisson arrival processes, and seasonal simulation.
- **Vulnerability & Disruption Scoring**: Value at Risk (VaR), Conditional Value at Risk (CVaR), and network bottleneck centrality.
- **Multi-Echelon Inventory Optimization**: Mixed-Integer Linear Programming (MILP) solving safety stock levels, holding costs, and stockout penalties.
- **Scenario Sensitivity Analysis**: Stress testing lead times and supplier disruption scenarios.

## Tech Stack

Python 3.11+, PuLP, SciPy, NumPy, Pandas, Pytest
