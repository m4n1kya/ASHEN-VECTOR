# Machine Learning Pipeline Architecture

This document describes the end-to-end machine learning pipeline used for alpha generation in ASHEN-VECTOR.

## Objective

The primary goal of the ML pipeline is to predict the forward $N$-day excess returns over a benchmark, avoiding absolute price prediction.

## Base Learners

We utilize a heterogeneous ensemble of base learners, favoring non-parametric tree-based models for tabular financial data.

