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

## Out-of-Sample Testing

Models are evaluated strictly on out-of-sample datasets that were entirely hidden during the hyperparameter tuning phase.

### Probability Calibration

Isotonic regression and Platt scaling are used to ensure model outputs represent true mathematical probabilities of market direction.

## Feature Importance

SHAP (SHapley Additive exPlanations) values are computed to ensure model interpretability and to guard against spurious correlations.

### LightGBM Implementation

LightGBM is highly effective for tabular financial data, capturing complex non-linear feature interactions efficiently.

### XGBoost Regularization

Strict L1 and L2 regularization penalties are applied to XGBoost models to maintain simplicity and prevent curve-fitting.

### Random Forest Bagging

Extremely Randomized Trees (ExtraTrees) are utilized to increase variance reduction and build robust ensemble consensus.

## Loss Functions

We optimize against custom, time-series specific loss functions rather than generic metrics like RMSE or cross-entropy.

### Asymmetric Loss

A custom asymmetric loss function heavily penalizes false positives (buying before a crash) compared to false negatives (missing a rally).

### Early Stopping

Dynamic learning rate decay and aggressive early stopping are implemented based on validation set performance to halt overfitting.

## Hyperparameter Optimization

Optuna is leveraged for distributed, Bayesian hyperparameter optimization across the purged cross-validation folds.

## Backtesting Integration

Model predictions are fed into an event-driven backtester that simulates execution delays and order book slippage.

### Transaction Costs

Strict, conservative transaction costs (commissions and spread crossing) are assumed during all validation phases.

### Risk-Adjusted Returns

Models are ultimately evaluated on their out-of-sample Sharpe and Sortino ratios, focusing on downside volatility.

### Information Ratio

The Information Ratio is tracked to evaluate the active return of the models relative to a standard benchmark like the S&P 500.

