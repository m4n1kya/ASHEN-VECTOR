# Data Engineering Pipeline

This document outlines the robust quantitative data pipeline built for ASHEN-VECTOR.

## Core Principles

The foundation of any quantitative model is its data. Our pipeline guarantees data integrity, point-in-time accuracy, and extreme computational efficiency.

## Qlib Integration

We leverage Microsoft Qlib for centralized dataset management, utilizing its optimized storage formats for fast time-series retrieval.

### Raw Data Ingestion

Daily OHLCV (Open, High, Low, Close, Volume) data is ingested from primary vendors via REST APIs and WebSocket streams.

### Timezone Standardization

All timestamps are strictly coerced to UTC, with market-specific trading hours applied to filter pre-market and after-hours noise.

## Data Cleaning

Missing values are a reality in finance. We never forward-fill target variables, but we do impute features carefully.

### Liquidity Filtering

The tradable universe is dynamically filtered to exclude illiquid micro-caps, enforcing a minimum 30-day average daily volume threshold.

### Survivor Bias Mitigation

Our historical datasets include delisted equities to ensure backtests do not suffer from survivor bias.

### Imputation Logic

Forward-filling is used exclusively for corporate actions, while backward-filling is strictly prohibited to prevent look-ahead bias.

## Corporate Actions

Stock splits and cash dividends are ingested daily to construct total return series seamlessly.

### Adjusted Prices

Adjusted close prices are calculated recursively to ensure that historical technical indicators remain mathematically sound post-split.

## Feature Engineering (Alpha Generation)

The system constructs hundreds of alpha factors across multiple time horizons.

### Momentum Features

Standard momentum oscillators including Relative Strength Index (RSI), MACD, and Rate of Change (ROC) are calculated using highly vectorized NumPy operations.

### Volatility Features

Average True Range (ATR) and Bollinger Band bandwidths are extracted to model heteroskedasticity and local market turbulence.

### Statistical Features

Rolling skewness and kurtosis are calculated to capture changes in the distribution of returns, indicating potential regime shifts.

### Cross-Sectional Ranking

Features are often ranked cross-sectionally (e.g., comparing AAPL's RSI against the entire S&P 500) to neutralize broad market movements.

## Feature Scaling

Rolling Z-Score normalization and Robust Scalers are applied to tame outliers without bleeding future distribution parameters into the training set.

## Target Variables

The primary target variable is the forward $N$-day return, adjusted for risk-free rates where necessary.

### Target Binning

For classification models, continuous returns are discretized into quantiles (e.g., top quartile vs bottom quartile) for robust meta-labeling.

## Feature Selection

Mutual Information and Spearman rank correlations are utilized to select features with the highest non-linear predictive power.

### Multicollinearity

Variance Inflation Factor (VIF) analysis purges highly correlated features to stabilize linear sub-models and reduce dimensionality.

### Principal Component Analysis

PCA is occasionally applied to extract orthogonal macroeconomic latent factors from highly correlated sector ETFs.

## Storage Architecture

Processed feature sets are serialized directly to Parquet formats, favoring column-oriented reads over legacy HDF5 structures.

### Memory Mapping

For deep learning models, extremely large datasets are memory-mapped (`mmap`) to bypass RAM constraints during batch generation.

### Caching Strategy

Intermediate feature engineering steps are cached using Redis and local filesystem hashes to drastically speed up iterative model tuning.

## Automation

A resilient CRON-based task scheduler triggers daily at market close to ingest, clean, and engineer the latest data points.

