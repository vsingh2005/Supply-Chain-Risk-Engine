# Supply-Chain-Risk-Engine

A Python tool for simulating supply chain disruptions, estimating stockout risk, and optimizing inventory shipment costs.

## What it does

- **Demand Simulation**: Generates stochastic demand paths using Geometric Brownian Motion and Poisson arrivals.
- **Risk Metrics**: Calculates Value at Risk (VaR) and Conditional VaR (expected shortfall) to model worst-case supplier delays.
- **Safety Stock Calculator**: Computes reorder points and safety stock levels based on lead-time uncertainty.
- **Cost Optimization**: Solves multi-warehouse shipping and allocation using mixed-integer linear programming (PuLP).

## Stack

Python, PuLP, NumPy, SciPy, Pandas