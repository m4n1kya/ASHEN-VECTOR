# Machine Learning Pipeline Architecture

This document describes the end-to-end machine learning pipeline used for alpha generation in ASHEN-VECTOR.

## Objective

The primary goal of the ML pipeline is to predict the forward $N$-day excess returns over a benchmark, avoiding absolute price prediction.

## Base Learners

We utilize a heterogeneous ensemble of base learners, favoring non-parametric tree-based models for tabular financial data.

### LightGBM

LightGBM is our primary model for dense feature interactions, configured with histogram-based binning to optimize training speed on CPU clusters.

#### Hyperparameters (LGBM)

Typical `num_leaves` are restricted strictly between 15 and 63 to aggressively combat the propensity of trees to overfit financial noise.

### XGBoost

XGBoost is maintained as a parallel learner, emphasizing exact greedy algorithms for smaller, high-signal feature subsets.

#### Regularization (XGB)

Alpha (L1) and Lambda (L2) penalties are aggressively tuned, often forcing sparsity in the leaf weights to drop collinear momentum indicators.

### Random Forest

Random Forests provide critical variance reduction, operating as a stabilizing force when gradient boosting methods become unstable during regime shifts.

#### ExtraTrees

Extremely Randomized Trees are employed to split nodes randomly, further decorating the trees and improving out-of-sample Sharpe ratios.

### Support Vector Machines

Non-linear SVMs with Radial Basis Function (RBF) kernels are used sparingly for classification tasks on highly dimensional PCA-reduced datasets.

### Deep Learning Constraints

While recurrent architectures (LSTMs) exist in the codebase, they are heavily constrained due to their extreme data hunger and risk of catastrophic forgetting.

#### Temporal Convolutional Networks

TCNs with dilated causal convolutions are preferred over LSTMs for extracting long-range dependencies in order book flow without look-ahead bias.

## Meta-Labeling (Secondary Models)

Following Marcos Lopez de Prado's framework, primary models predict direction, while secondary models predict the probability of the primary model being correct.

### Primary Signal

The primary model generates a continuous score $[-1, 1]$ indicating the expected strength of the directional move.

### Secondary Sizing

The secondary classification model uses the primary signal along with market volatility as features to output an optimal Kelly fraction for position sizing.

## Feature Preprocessing

To achieve stationarity without destroying memory, price series are fractionally differentiated rather than integer differenced.

### Scaling

Features are normalized using Scikit-Learn's `RobustScaler`, prioritizing median and interquartile ranges over mean and variance to ignore fat-tailed anomalies.

#### Rolling Normalization

To prevent data leakage, all scaling parameters are fitted on a strict rolling window trailing the training set, never using future global statistics.

## Cross Validation Strategy

Standard K-Fold is strictly forbidden. The pipeline implements Purged Walk-Forward Cross Validation.

### Combinatorial Purged CV

To maximize the number of testing paths, we simulate multiple historical trajectories using Combinatorial Purged Cross Validation (CPCV).

#### Embargo Period

A 5-day embargo period is strictly enforced after each training block to ensure multi-day return labels do not bleed into the validation fold.

## Hyperparameter Tuning

Hyperparameter spaces are searched using Bayesian Optimization via the Optuna framework, focusing on expected improvement over random search.

### Trial Pruning

Optuna's Median Pruner automatically terminates training trials that show poor early validation performance, saving massive amounts of compute time.

## Loss Functions

The ML pipeline implements custom loss functions rather than standard Mean Squared Error (MSE).

### Asymmetric Penalty

The custom gradient heavily penalizes 'wrong-way risk'—predicting a massive rally when the asset actually crashes.

### Sharpe Ratio Validation

Models are early-stopped based on their validation Sharpe ratio, ensuring we optimize for risk-adjusted returns, not just raw accuracy.

## Model Registry

All trained models, their hyperparameters, and serialized artifacts are tracked in an internal registry powered by MLflow.

### Serialization

Tree-based models are exported using Joblib, while neural networks are exported to ONNX format for high-speed C++ inference in live trading.

### Lifecycle States

Models move through strict states: `Experiment` -> `Staging` (Paper Trading) -> `Production` (Live Execution) -> `Archived`.

## Model Decay & Drift

Financial regimes shift rapidly. The pipeline constantly monitors for concept drift and statistical degradation.

