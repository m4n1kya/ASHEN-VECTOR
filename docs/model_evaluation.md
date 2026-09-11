# Model Evaluation and Validation Framework

This document details the rigorous machine learning evaluation protocols used in ASHEN-VECTOR.

## Core Principles

In quantitative finance, rigorous validation is required to prevent overfitting to historical noise and to ensure out-of-sample generalization.

### Look-Ahead Bias

Strict pipeline constraints are enforced to guarantee that no future data leaks into the training sets of our predictive models.

## Purged Walk-Forward Cross-Validation

We utilize a purged walk-forward methodology to respect the temporal nature of financial time-series data.

### Embargoing

An embargo period is applied after the training set to prevent overlap between training and testing periods caused by multi-day return calculations.

### Combinatorial Purged CV

CPCV is employed to generate multiple backtest paths, allowing us to estimate the probability of backtest overfitting.

