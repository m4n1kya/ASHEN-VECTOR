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

