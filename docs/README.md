# ASHEN-VECTOR Technical Documentation

Welcome to the architectural and quantitative methodology documentation for **ASHEN-VECTOR**.

---

## Documentation Index

### 1. System & Infrastructure Architecture
- [System Architecture Overview](./system_architecture.md) — End-to-end service topology, data flow, and Architectural Decision Records (ADRs)
- [Core Architecture Notes](./architecture.md) — High-level platform modularization and design principles
- [API Reference Architecture](./api_reference.md) — FastAPI REST endpoints, schemas, and request/response lifecycles
- [Deployment & Infrastructure](./deployment_architecture.md) — Containerization, orchestration, and production deployment topology
- [Security Architecture](./security_architecture.md) — Input validation, runtime hardening, and defense-in-depth safeguards

### 2. Quantitative Research & Mathematical Models
- [Quantitative Research Methodology](./quantitative_research_methodology.md) — Alpha hypothesis testing, IC/ICIR metrics, and factor neutralization
- [Quantitative Trading Strategies](./quantitative_trading_strategies.md) — Multi-horizon momentum, Ornstein-Uhlenbeck mean reversion, Fama-French 5-Factor, and HMM regimes
- [Machine Learning Pipeline](./machine_learning_pipeline.md) — LightGBM, XGBoost, and Random Forest ensemble architecture
- [Live Model Execution Mechanics](./model_working.md) — Real-time feature extraction, scoring, and consensus aggregation
- [Model Evaluation & Validation](./model_evaluation.md) — Purged walk-forward cross-validation, embargoing, and probability calibration
- [Sentiment Analysis & NLP](./sentiment_analysis.md) — Financial text processing and sentiment factor integration

### 3. Data Engineering & Governance
- [Data Engineering Pipeline](./data_engineering.md) — Qlib binary store integration, OHLCV normalization, and technical indicators
- [Market Data Ingestion Pipeline](./market_data_pipeline.md) — Dual-source data provider and deterministic GBM simulation engine
- [Data Governance & Lineage](./data_governance.md) — Point-in-time correctness, survivorship bias mitigation, and quality gates

### 4. Backtesting, Execution & Risk Management
- [Event-Driven Backtesting Engine](./backtesting_engine.md) — Walk-forward simulation, transaction cost modeling, and benchmark comparison
- [Trade Execution Algorithms](./execution_algorithms.md) — Slippage modeling, VWAP/TWAP scheduling, and implementation shortfall
- [Risk Management Framework](./risk_framework.md) — Value at Risk (VaR), Expected Shortfall (CVaR), and drawdown controls
- [Portfolio Optimization](./portfolio_optimization.md) — Mean-variance optimization, volatility targeting, and position sizing
- [Regulatory Compliance & Reporting](./compliance_reporting.md) — Audit trails, pre-trade risk gates, and performance attribution

### 5. Frontend & Quality Engineering
- [UI/UX Design System](./ui_ux_design_system.md) — Institutional dark-theme color tokens, typography, and layout architecture
- [UI Performance Optimization](./ui_performance_optimization.md) — Rendering optimization, memoization boundaries, and chart responsiveness
- [Backend Testing Framework](./backend_testing.md) — Unit and integration test suites, fixtures, and coverage standards
