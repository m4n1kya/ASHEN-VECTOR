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

