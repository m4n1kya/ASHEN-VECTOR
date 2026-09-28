# Quantitative Trading Strategies

This document catalogs the proprietary alpha-generating strategies deployed by the ASHEN-VECTOR execution engine.

## Statistical Arbitrage (StatArb)

The core StatArb framework relies on identifying temporary pricing inefficiencies across highly correlated assets using cointegration tests.

### Dispersion Trading

We trade the implied versus realized correlation by taking positions in an index ETF against a basket of its underlying constituents.

### Volatility Surface Arbitrage

Algorithms scan the options chain for localized mispricings on the volatility surface, exploiting violations of put-call parity.

## Momentum and Trend

Cross-asset momentum signals are generated using dual-moving average crossovers filtered by ADX (Average Directional Index) to confirm trend strength.

### ML Pairs Selection

An unsupervised clustering algorithm (DBSCAN) groups thousands of equities by fundamental and price-action features to discover novel trading pairs.

### Regime Switching (HMM)

A Gaussian Hidden Markov Model detects shifts between 'bull', 'bear', and 'sideways' regimes, dynamically adjusting the portfolio beta.

## Intraday Mean Reversion

This strategy fades extreme intraday deviations from the Volume Weighted Average Price (VWAP) assuming mean reversion before the market close.

