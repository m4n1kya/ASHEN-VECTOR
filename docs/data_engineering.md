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

