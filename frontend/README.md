# ASHEN-VECTOR — Frontend Research Terminal

The **ASHEN-VECTOR** web interface is an institutional-grade quantitative research terminal built with **Next.js (App Router)**, **TypeScript**, **Tailwind CSS**, and **Recharts**.

---

## Architecture & Routes

| Route | Module | Description |
|---|---|---|
| `/dashboard` | `src/app/dashboard/` | Command-center stock intelligence view, mathematical stack grid, consensus radar, and HMM regime bar charts |
| `/research` | `src/app/research/` | Deep-dive quantitative factor and statistical research interface |
| `/models` | `src/app/models/` | Multi-model ensemble consensus breakdown and evidence quality metrics |
| `/validation` | `src/app/validation/` | Out-of-sample Purged Walk-Forward Cross-Validation runner, calibration curves, and fold stability |
| `/backtest` | `src/app/backtest/` | Event-driven backtesting configuration, equity curves, and benchmark comparison |
| `/risk` | `src/app/risk/` | Volatility regime analysis, drawdown profile, and risk-adjusted return diagnostics |
| `/stocks/[symbol]` | `src/app/stocks/[symbol]/` | Instrument-level quantitative stack and multi-model consensus view |

---

## Development

```bash
# Install dependencies
npm install

# Start development server (http://localhost:3000)
npm run dev

# Production build & type-check
npm run build
npm start
```

> **Note:** Ensure the ASHEN-VECTOR FastAPI backend is running on `http://127.0.0.1:8000` before launching the frontend terminal.
