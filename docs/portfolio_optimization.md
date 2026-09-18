# Portfolio Optimization Framework

This document details the portfolio construction and optimization mathematics powering ASHEN-VECTOR.

## Core Principles

We utilize advanced adaptations of Modern Portfolio Theory (MPT) to translate raw predictive alpha into a mathematically optimal portfolio of weights.

## Mean-Variance Optimization

The primary objective function seeks to maximize the expected return of the portfolio subject to a strict upper bound on portfolio variance (volatility).

### Black-Litterman Integration

To prevent the extreme corner solutions typical of naive MVO, we implement the Black-Litterman model, treating the ML predictions as absolute views.

## Covariance Estimation

The optimization engine relies heavily on an accurate, forward-looking covariance matrix estimated from the trailing 252 days of daily returns.

### Ledoit-Wolf Shrinkage

To ensure the covariance matrix is well-conditioned and invertible, Ledoit-Wolf shrinkage is applied, shrinking the sample covariance toward a constant correlation target.

## Expected Returns Vector

The vector of expected returns is directly populated by the primary output of the ML ensemble, dynamically scaled by the Kelly fraction.

## Risk Parity Allocation

As a fallback to MVO, the system can dynamically switch to a Risk Parity algorithm, ensuring that every asset contributes equally to the total portfolio risk.

### Inverse Volatility Weighting

For subsets of highly correlated assets, naive inverse-volatility weighting is utilized to quickly penalize assets experiencing sudden volatility spikes.

## Optimization Constraints

The quadratic solver enforces strict L1-norm turnover constraints, ensuring the proposed rebalance does not incur transaction costs that exceed the expected alpha.

### Concentration Limits

No single position may exceed 8% of total equity, and net sector exposure is capped at 25% to prevent unintended macroeconomic factor bets.

### Short Selling & Margin

The optimizer natively supports long-short portfolios (130/30), tracking the required initial margin to ensure the portfolio remains solvent under stress.

## Solver Engine (OSQP)

The convex optimization problem is passed to the OSQP (Operator Splitting Quadratic Program) solver, which typically converges in under 5 milliseconds.

## Rebalancing Logic

Rebalancing is not purely calendar-based. It is triggered asynchronously when the current portfolio weights drift beyond a 2% tracking error from the optimal weights.

### Fractional Shares

Continuous optimal weights are discretely mapped to actual share counts, utilizing fractional share logic where supported by the execution broker.

## Execution Shortfall

The realized execution prices of the rebalanced portfolio are tracked against the VWAP (Volume-Weighted Average Price) to measure implementation shortfall.

