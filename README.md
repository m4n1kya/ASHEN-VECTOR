# ASHEN-VECTOR

**Quantitative Market Intelligence Platform**

ASHEN-VECTOR is an experimental quantitative market intelligence and systematic research platform built around Qlib-compatible market data infrastructure. It provides a modular architecture for quantitative factor research, statistical analysis, machine learning–based prediction, probability calibration, and systematic backtesting.

> **Status:** Early development — Phase 1 (Foundation).

---

## Overview

ASHEN-VECTOR is designed as a personal quantitative research terminal. Given an instrument identifier, the platform delivers:

- **Market Data** — Historical OHLCV price series from the Qlib data engine
- **Statistical Analysis** — Returns, volatility, drawdown, Sharpe, Sortino, and other quantitative metrics
- **Technical Indicators** — SMA, EMA, RSI, MACD, Bollinger Bands, ATR, momentum
- **Quantitative Factor Scores** — Momentum, trend, volatility, liquidity, mean reversion composites
- **ML Predictions** — Directional probability, expected return, prediction intervals *(Phase 3+)*
- **Confidence Calibration** — Platt scaling / isotonic regression on model probabilities *(Phase 4+)*
- **Backtesting** — Walk-forward strategy evaluation with realistic assumptions *(Phase 6+)*
- **Model Explainability** — SHAP-based feature contribution analysis *(Phase 4+)*

All predictions are clearly labeled as model-derived estimates. The platform never fabricates confidence scores or presents predictions as guaranteed outcomes.

---

## Architecture

```
Market Data (Qlib)
  → Feature Engineering
    → Quantitative Factors
      → ML Models
        → Calibrated Predictions
          → Risk Assessment
            → Signal Generation
              → Dashboard
```

```
ASHEN-VECTOR/
├── src/ashen_vector/       # Core application
│   ├── api/                # FastAPI REST endpoints
│   ├── config/             # Pydantic settings
│   ├── core/               # Exceptions, shared types
│   ├── data/               # Qlib provider, instrument service
│   ├── features/           # Technical indicator calculations
│   ├── analytics/          # Statistical analysis
│   └── models/             # Model registry and training (Phase 3+)
├── scripts/                # CLI tools (inspect, train, evaluate, backtest)
├── configs/                # YAML configuration files
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation
└── frontend/               # Next.js dashboard (Phase 5+)
```

---

## Tech Stack

| Layer      | Technology                                  |
|------------|---------------------------------------------|
| Data       | Microsoft Qlib, pandas, NumPy               |
| Backend    | Python 3.12, FastAPI, Pydantic, Uvicorn     |
| ML         | scikit-learn, LightGBM, XGBoost *(planned)* |
| Frontend   | Next.js, TypeScript, Tailwind *(planned)*   |
| Storage    | SQLite *(planned)*                          |

---

## Setup

### Prerequisites

- Python 3.12+
- Qlib binary dataset (pre-initialized, ~5 GB)
- Qlib source (adjacent directory)

### Installation

```bash
# Clone the repository
git clone <repository-url> ASHEN-VECTOR
cd ASHEN-VECTOR

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install ASHEN-VECTOR and dependencies
pip install -e ".[dev]"

# Install Qlib from adjacent source
pip install -e ../qlib
```

### Configuration

Copy the example environment file and adjust paths:

```bash
cp .env.example .env
```

Key variables in `.env`:

| Variable             | Description                          | Default            |
|----------------------|--------------------------------------|--------------------|
| `QLIB_PROVIDER_URI`  | Path to Qlib binary dataset          | `../qlib/qlib_bin` |
| `QLIB_REGION`        | Qlib market region                   | `us`               |
| `API_HOST`           | API server host                      | `127.0.0.1`        |
| `API_PORT`           | API server port                      | `8000`             |

The `QLIB_PROVIDER_URI` is resolved relative to the project root. The Qlib dataset must **not** be stored inside the ASHEN-VECTOR repository.

---

## Usage

### Inspect Dataset

```bash
python scripts/inspect_data.py
python scripts/inspect_data.py --symbol SH600000
```

### Run API Server

```bash
python -m uvicorn src.ashen_vector.api.main:app --reload
```

### API Endpoints (Phase 1)

| Method | Endpoint                          | Description                    |
|--------|-----------------------------------|--------------------------------|
| GET    | `/api/health`                     | System health check            |
| GET    | `/api/instruments`                | List available instruments     |
| GET    | `/api/instruments/{symbol}`       | Instrument details             |
| GET    | `/api/stocks/{symbol}/history`    | Historical OHLCV data          |
| POST   | `/api/predict`                    | Prediction *(MODEL_NOT_READY)* |

### Run Tests

```bash
pytest
```

---

## Current Capabilities (Phase 1)

- [x] Qlib data provider with singleton initialization
- [x] Instrument discovery and validation
- [x] Historical OHLCV data retrieval via REST API
- [x] Technical indicator library (SMA, EMA, RSI, MACD, Bollinger, ATR, momentum)
- [x] Financial statistics engine (returns, volatility, drawdown, Sharpe, Sortino)
- [x] Model registry architecture
- [x] Health monitoring endpoint
- [x] Environment-based configuration

## Roadmap

- [ ] **Phase 2** — Feature engineering pipeline, instrument APIs expansion
- [ ] **Phase 3** — LightGBM classifier/regressor, training pipeline
- [ ] **Phase 4** — Prediction API, probability calibration, SHAP explanations
- [ ] **Phase 5** — Next.js dashboard, stock analysis page, charts
- [ ] **Phase 6** — Backtesting engine, walk-forward evaluation
- [ ] **Phase 7** — Prediction history, experiment tracking
- [ ] **Phase 8** — Polish, documentation, performance optimization

---

## Research Philosophy

> Extract signal from noise through mathematics, statistics, and systematic experimentation.

ASHEN-VECTOR is a research instrument, not a marketing dashboard. If a model performs poorly, the platform reports that it performs poorly. All metrics, confidence scores, and predictions are derived from validated statistical methods — never fabricated for visual appeal.

---

## Limitations

- This is an **experimental research platform**, not production trading software.
- Predictions are **model estimates**, not guaranteed outcomes.
- No real-time data feed — operates on historical Qlib datasets.
- No portfolio management or order execution.
- Model performance may not generalize to unseen market conditions.

---

## Credits

- **Qlib** — Microsoft's open-source quantitative research platform, used as the underlying data engine and quantitative infrastructure. [github.com/microsoft/qlib](https://github.com/microsoft/qlib)

---

*ASHEN-VECTOR — Quantitative Market Intelligence*
