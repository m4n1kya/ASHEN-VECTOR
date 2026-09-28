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

### Index Rebalancing

The system predicts Russell and S&P index reconstitution events, accumulating positions in likely additions before the official announcement.

## Options Market Making

Gamma scalping is employed on long straddle positions, dynamically hedging delta as the underlying price fluctuates to capture realized volatility.

### Volatility Risk Premium

A persistent short-volatility strategy harvests the roll yield from the contango term structure of VIX futures, protected by deep out-of-the-money calls.

## High-Frequency Trading (HFT)

Market making algorithms continuously quote bid/ask spreads, utilizing the Avellaneda-Stoikov model to manage inventory risk.

### Adverse Selection Mitigation

Order Flow Imbalance (OFI) metrics at the top of the book are used to pull resting limit orders milliseconds before toxic flow sweeps the book.

## Event-Driven Strategies

The Post-Earnings Announcement Drift (PEAD) strategy goes long on stocks with massive positive earnings surprises, capturing the multi-day drift.

### Macro Shock Absorber

During scheduled CPI or FOMC releases, the engine widens spreads and switches to a momentum-ignition strategy to ride the initial volatility spike.

## Factor Investing

A Market-Neutral Long/Short equity book is constructed using Fama-French style factors (Value, Size, Quality, Momentum) neutralized for sector risk.

## Crypto Arbitrage

Triangular arbitrage bots monitor Binance, Kraken, and Coinbase via WebSockets, executing riskless cyclic trades when price disparities exceed fee thresholds.

