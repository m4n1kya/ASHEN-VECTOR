# Contributing to ASHEN-VECTOR

Thank you for your interest in contributing to **ASHEN-VECTOR**.

---

## Core Engineering Principles

1. **Zero Look-Ahead Bias**: Any modification to `src/ashen_vector/features/`, `models/`, or `backtesting/` must strictly preserve temporal ordering. Feature scalers, rolling statistics, and cross-validation splits must never access future timestamps ($t + k$).
2. **No Fabricated Metrics**: All model probabilities, reliability scores, Sharpe ratios, and drawdown figures surfaced to the API or UI must originate from deterministic mathematical or statistical computation.
3. **Separation of Concerns**: Mathematical and quantitative logic belongs in the Python backend (`src/ashen_vector/`). The Next.js frontend (`frontend/`) is strictly responsible for presentation, visualization, and interactive exploration.

---

## Development Workflow

1. **Fork & Branch**: Create a feature branch from `main` (`feat/your-feature` or `fix/your-fix`).
2. **Install Dependencies**:
   ```bash
   pip install -e ".[dev,ml]"
   cd frontend && npm install
   ```
3. **Run Verification Suite**:
   ```bash
   PYTHONPATH=src pytest tests/unit tests/test_live_market.py -v
   cd frontend && npx tsc --noEmit
   ```
4. **Commit Convention**: Use Conventional Commits (`feat:`, `fix:`, `arch:`, `research:`, `perf:`, `test:`, `docs:`).
5. **Pull Request**: Open a pull request against `main` with a clear summary of methodology and test coverage.
