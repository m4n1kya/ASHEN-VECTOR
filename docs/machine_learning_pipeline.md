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

