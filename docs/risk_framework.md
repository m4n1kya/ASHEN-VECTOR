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

