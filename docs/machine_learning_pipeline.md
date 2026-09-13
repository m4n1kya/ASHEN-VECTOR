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

