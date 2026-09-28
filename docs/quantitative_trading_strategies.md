# Quantitative Trading Strategies

This document catalogs the proprietary alpha-generating strategies deployed by the ASHEN-VECTOR execution engine.

## Statistical Arbitrage (StatArb)

The core StatArb framework relies on identifying temporary pricing inefficiencies across highly correlated assets using cointegration tests.

### Dispersion Trading

We trade the implied versus realized correlation by taking positions in an index ETF against a basket of its underlying constituents.

### Volatility Surface Arbitrage

Algorithms scan the options chain for localized mispricings on the volatility surface, exploiting violations of put-call parity.

