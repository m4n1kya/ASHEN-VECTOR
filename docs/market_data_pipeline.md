# Market Data Ingestion Pipeline

This document outlines the market data ingestion engine and deterministic simulation fallback architecture used in ASHEN-VECTOR.

---

## 1. Dual-Source Data Architecture

ASHEN-VECTOR uses a two-tier market data layer:

1. **Primary Institutional Store (Qlib Binary Provider)**
   - Point-in-time historical OHLCV datasets stored in optimized column-binary format (`qlib_bin`).
   - Managed by `src/ashen_vector/data/qlib_provider.py` and `instrument_service.py`.
   - Provides sub-millisecond historical slicing across constituents without look-ahead leakage.

2. **Live & Deterministic Simulation Engine (`LiveMarketService`)**
   - Managed by `src/ashen_vector/api/services/live_market.py`.
   - Eliminates external rate-limit bottlenecks and third-party API instability by providing a deterministic Geometric Brownian Motion (GBM) + Jump Diffusion engine seeded per instrument ticker.

---

## 2. Mathematical Formulation

### Geometric Brownian Motion (GBM)
Daily price trajectories follow the stochastic differential equation:

$$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$$

With discrete daily log-return increments over horizon $\Delta t = \frac{1}{252}$:

$$S_{t} = S_{t-1} \exp\left(\left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma\sqrt{\Delta t}\, Z_t\right), \quad Z_t \sim \mathcal{N}(0, 1)$$

### Deterministic Symbol Seeding
Random number generation is deterministically seeded from the canonical ticker symbol hash. Querying the same symbol across sessions yields identical 5-year (1,260 trading day) time-series trajectories while preserving cross-sectional independence across symbols.

### OHLCV Structural Invariants
Every generated bar is validated against market microstructure invariants:
- $\text{High}_t \ge \max(\text{Open}_t, \text{Close}_t)$
- $\text{Low}_t \le \min(\text{Open}_t, \text{Close}_t)$
- $S_t > 0 \quad \forall t$
- $\text{Volume}_t \sim \text{LogNormal}(\mu_v, \sigma_v^2)$

---

## 3. Risk & Reliability Pipeline Integration

Once the 1,260-day OHLCV frame is assembled, `LiveMarketService` pipelines the series into:
1. **`LiveModelEngine`** (`live_models.py`) — Executes the 7-model quantitative stack (LightGBM, XGBoost, Random Forest, Momentum Z-Score, ARIMA, GARCH(1,1), and Gaussian HMM Regime Detection).
2. **`ReliabilityEngine`** (`reliability_engine.py`) — Computes the out-of-sample Ashen Reliability Score (ARS) across Brier calibration, ROC-AUC, fold stability, and regime coverage.

---

## 4. Verification Suite

The ingestion and analysis pipeline is verified by 21 unit and integration assertions in `tests/test_live_market.py`, covering schema completeness, trading-day count, timezone normalization, OHLC bounds, deterministic reproducibility, drawdown bounds, and ensemble consensus payloads.
