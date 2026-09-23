# Quantitative Research Methodology

This document codifies the rigorous, evidence-based research process used to discover, validate, and deploy alpha-generating strategies.

## Alpha Hypothesis Generation

Every strategy begins with a falsifiable economic hypothesis grounded in behavioral finance, microstructure theory, or macroeconomic logic.

## Universe Construction

The investable universe is filtered to liquid, mid-to-large cap equities with a minimum 60-day ADTV of $10M to ensure execution feasibility.

### Liquidity Filters

Stocks with bid-ask spreads exceeding 50 basis points are excluded, as transaction costs would consume the projected alpha entirely.

### Survivorship Bias

The universe includes all historically listed instruments, including delisted and bankrupt companies, to prevent survivorship bias from inflating backtested returns.

## Signal Taxonomy

Alpha signals are classified into four families: Momentum (trend-following), Reversion (mean-reverting), Quality (fundamental), and Sentiment (behavioral).

### Price-Based Signals

Price momentum signals are constructed as exponentially weighted returns over 5, 21, 63, and 252-day windows, normalized by realized volatility.

