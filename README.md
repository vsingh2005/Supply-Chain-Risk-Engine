# Supply-Chain-Risk-Engine

A quantitative modeling and optimization engine for simulating supply chain disruptions, evaluating inventory tail risk metrics, and solving multi-facility logistics allocation problems under uncertainty.

## Overview

Global supply networks are vulnerable to stochastic demand fluctuations, lead-time volatility, and catastrophic supplier outages. Relying solely on deterministic safety stock formulas and mean averages frequently underestimates tail risks, leading to costly stockouts or bloated carrying costs.

This project implements an operations research toolkit that models non-linear demand paths, quantifies extreme downside risk using Value at Risk (VaR) and Conditional Value at Risk (CVaR), and formulates multi-echelon cost optimization problems as Mixed-Integer Linear Programs (MILP).

## Architecture

```
+-----------------------------------------------------------+
| Stochastic Demand & Disruption Simulation                 |
|  - Geometric Brownian Motion (GBM) with Poisson Jumps     |
|  - Markov Chain Supplier Failure & Recovery Dynamics      |
|  - Gaussian Copula for Correlated Disruptions             |
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
| Risk Evaluation Layer                                     |
|  - Value at Risk (VaR) & Conditional VaR (CVaR / ES)      |
|  - Reorder Point & Dynamic Safety Stock Calculation       |
|  - Multi-Echelon Clark-Scarf Inventory Sizing             |
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
| Optimization Engine                                       |
|  - Mixed-Integer Linear Programming (PuLP / CBC Solver)   |
|  - Capacitated Facility Location Allocation               |
|  - Network Digraph & Betweenness Centrality Bottlenecks   |
+-----------------------------------------------------------+
```

## Core Modules and Engineering Details

- **Stochastic Demand Simulation (`simulation.py`)**: Models lead-time demand using Geometric Brownian Motion (GBM) with configurable drift and volatility parameters, augmented by discrete Poisson arrival processes to capture sudden demand spikes.
- **Tail Risk Metrics (`metrics.py`)**: Computes empirical Value at Risk (VaR) and Conditional Value at Risk (CVaR / Expected Shortfall) at a 95% confidence level across Monte Carlo simulation paths. CVaR calculates the expectation of losses in the worst 5% tail, providing an accurate metric for severe disruption events.
- **Inventory Sizing & Reorder Logic (`lead_time.py`, `newsvendor.py`, `eoq.py`)**: Implements dynamic reorder point calculation incorporating joint demand and lead-time variances, stochastic newsvendor models with critical fractile optimization, and Economic Order Quantity (EOQ) with quantity discounts.
- **Mixed-Integer Linear Programming (`inventory.py`, `facility_location.py`)**: Formulates multi-warehouse shipment allocation and capacitated facility location as mixed-integer linear programs using PuLP, solved with the CBC branch-and-cut solver to minimize total logistics and holding costs under capacity constraints.
- **Network Topology & Bottleneck Detection (`network_graph.py`)**: Constructs directed acyclic supply network graphs and computes betweenness centrality scores to identify critical supplier nodes whose failure would disproportionately disconnect downstream distribution.
- **Correlated Disruption Modeling (`copula.py`, `disruption.py`)**: Models multi-supplier dependency using Gaussian copulas to capture systemic regional shocks where supplier failures are correlated rather than independent.

## Technical Decisions

- **Why CVaR over Standard Deviation**: Standard deviation treats positive and negative deviations symmetrically and fails to quantify tail heaviness. CVaR provides a coherent risk measure that focuses specifically on the severity of catastrophic losses.
- **Why Mixed-Integer Linear Programming**: Greedy heuristic dispatchers can become trapped in local optima when facility opening fixed costs and transport tariffs conflict. MILP guarantees globally optimal network routing while respecting hard capacity limits.
- **Why Markov State Transitions for Suppliers**: Component suppliers experience stateful recovery periods following disruptions rather than instantaneous resets. A two-state Markov chain (Operational vs. Disrupted) accurately models Mean Time Between Failures (MTBF) and Mean Time to Repair (MTTR).

## Technology Stack

- **Language**: Python 3.11+
- **Optimization**: PuLP (MILP / CBC Solver)
- **Numerical Computing**: NumPy, SciPy
- **Data Manipulation**: Pandas
- **Testing**: Pytest, Pytest-Cov

## Project Structure

```
supply-chain-risk-engine/
├── src/
│   └── supply_chain_risk/
│       ├── simulation.py        # GBM and Poisson Monte Carlo demand simulation
│       ├── metrics.py           # VaR and CVaR tail risk calculators
│       ├── inventory.py         # MILP warehouse allocation model
│       ├── facility_location.py # Capacitated facility location optimization
│       ├── network_graph.py     # Supply network digraph and betweenness analysis
│       ├── copula.py            # Gaussian copula for correlated disruptions
│       ├── disruption.py        # Markov chain supplier failure dynamics
│       ├── lead_time.py         # Safety stock and reorder point formulas
│       ├── newsvendor.py        # Stochastic newsvendor fractile models
│       └── eoq.py               # Economic Order Quantity calculations
├── tests/                       # Unit and optimization validation tests
├── pyproject.toml               # Package configuration
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git

### Installation

```bash
git clone https://github.com/vsingh2005/Supply-Chain-Risk-Engine.git
cd Supply-Chain-Risk-Engine
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -e .
```

### Running Tests

```bash
pytest tests/ -v
```