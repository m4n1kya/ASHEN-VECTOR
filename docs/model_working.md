# Live Model Execution Mechanics

This document details the real-time execution mechanics of the predictive models within ASHEN-VECTOR.

## End-to-End Flow

The inference pipeline transforms raw tick data into a probabilistically weighted execution order in under 450 milliseconds.

## Feature Extraction

Incoming FIX streams are parsed, and continuous features (like order book imbalance and tick volatility) are updated in memory without hitting disk.

### OHLCV Vectorization

Real-time OHLCV bars are constructed dynamically, utilizing Numba JIT-compiled functions to calculate rolling momentums and Z-scores instantly.

## Pre-processing Layer

Incoming features are scaled against the trailing 252-day distributions held in Redis. Missing ticks are interpolated using cubic splines.

## ONNX Runtime Execution

The primary tree models (LightGBM/XGBoost) are executed via the C++ ONNX Runtime, bypassing Python's Global Interpreter Lock (GIL) for parallel scoring.

### Base Scoring

Model outputs are returned as tensors representing the raw log-odds of a directional market move over the target horizon.

## Meta-Labeling & Sizing

A secondary meta-model evaluates the primary model's confidence, applying the Kelly Criterion to output a recommended position size fraction.

