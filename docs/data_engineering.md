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

