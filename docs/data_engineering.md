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

