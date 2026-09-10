# Risk Management Framework

This document outlines the comprehensive risk management framework implemented in ASHEN-VECTOR.

## Core Philosophy

Our primary objective is capital preservation during tail-risk events while maintaining optimal exposure to alpha-generating factors.

## Value at Risk (VaR)

VaR is computed daily at the 95% and 99% confidence intervals using a rolling 252-day historical window.

### Expected Shortfall (CVaR)

We prioritize Conditional VaR over traditional VaR to better estimate the expected loss severity in the left tail of the distribution.

### Simulation Methodologies

The system utilizes both non-parametric historical simulation and parametric GARCH-based volatility modeling for robust estimates.

## Portfolio Volatility

Dynamic correlation matrices are updated intraday to prevent unintended concentration risk across asset classes.

### Drawdown Monitoring

Maximum Drawdown (MDD) thresholds are strictly enforced, with automated exposure reduction triggered at specific drawdown watermarks.

## Stress Testing

Historical scenarios (e.g., 2008 Financial Crisis, 2020 COVID Crash) and Monte Carlo simulations are run weekly to stress-test the portfolio.

### Beta Exposure

The portfolio aims for market neutrality, keeping net SPY beta between -0.1 and +0.1 to isolate idiosyncratic alpha.

## Position Sizing

We utilize volatility-scaled position sizing (target volatility) to ensure equal risk contribution across all active trades.

### Liquidity Constraints

Positions are capped at a maximum of 1% of the asset's average 30-day daily trading volume to ensure execution efficiency.

## Factor Exposure

Gross exposure to Fama-French factors (SMB, HML, Momentum) is continuously monitored to avoid unintentional factor tilts.

### Tail Risk Hedging

A small allocation to deep out-of-the-money VIX calls and SPY puts acts as an insurance overlay during regime shifts.

## Regime Detection

Hidden Markov Models (HMM) are employed to identify high-volatility regimes, automatically tightening stop-losses across the board.

## Conclusion

Strict adherence to this framework ensures the longevity and stability of the ASHEN-VECTOR quantitative ecosystem.
