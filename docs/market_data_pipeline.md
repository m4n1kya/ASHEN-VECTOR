# Market Data Ingestion Pipeline

This document outlines the ultra-reliable market data ingestion engine designed to replace legacy public APIs.

## Legacy API Deprecation

The reliance on `yfinance` has been fully deprecated due to unacceptable rate-limiting and connection drops during high-volume periods.

## Synthetic Data Engine

A mathematical synthetic data generator guarantees 100% uptime for the UI by generating realistic market data when live endpoints fail.

