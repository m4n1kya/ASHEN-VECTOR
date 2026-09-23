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

### Short Interest Signals

Short Interest Ratio (SIR) is computed as shares short divided by average daily volume, serving as a contrarian indicator for crowded shorts.

### Earnings Revision Momentum

Earnings Revision Momentum (ERM) captures the rate of change in analyst EPS estimates, exploiting the documented underreaction to estimate revisions.

### Analyst Dispersion

High standard deviation in analyst EPS estimates signals fundamental uncertainty; low dispersion paired with positive revision is a high-conviction buy signal.

### Insider Transaction Signals

Clustered buying by C-suite insiders within 10 days of each other is treated as a high-conviction bullish signal, weighted by transaction dollar amount.

### Innovation Signals

R&D intensity (R&D expense / revenue) and patent filing velocity are used as slow-moving quality signals for identifying compounders.

### Commodity Sensitivity

Rolling 90-day correlations between stock returns and key commodity prices (WTI, copper, gold) create sector-aware macro hedging signals.

## Factor Neutralization

Raw alpha signals are orthogonalized against known systematic risk factors (market beta, size, value) to isolate the idiosyncratic component.

### Gram-Schmidt Process

The Gram-Schmidt process is applied iteratively to remove linear dependencies between alpha signals and the Fama-French five-factor space.

### Sector Neutralization

Signals are de-meaned at the GICS sector level to prevent the strategy from expressing unintended sector bets rather than stock-specific alpha.

### Size Neutralization

Signals are z-scored separately within large-cap, mid-cap, and small-cap buckets, ensuring performance is not driven by a size tilt.

## Signal Decay Analysis

Alpha signal half-life is measured by computing the autocorrelation of forward returns conditioned on the signal rank, identifying the optimal holding period.

### Information Decay Curves

Information Coefficient (IC) is computed at 1, 5, 10, 21, and 63-day forward horizons to map the complete signal decay curve.

### Rebalancing Frequency

The rebalancing frequency is set at the point where marginal alpha gain from more frequent rebalancing is outweighed by incremental transaction costs.

## Signal-to-Noise Analysis

The signal-to-noise ratio is quantified by the ratio of the mean IC to the standard deviation of IC across rolling 63-day windows.

### IC Calculation

Spearman Rank IC is used instead of Pearson IC to achieve robustness against outliers in both the signal and the forward return distribution.

### ICIR Metric

The ICIR (IC mean / IC standard deviation) is the primary signal quality filter; signals with ICIR below 0.5 are rejected before backtesting.

## Quintile Portfolio Analysis

Raw signals are ranked into quintiles. The spread in average forward returns between Q1 (bottom) and Q5 (top) quantifies the raw alpha power.

### Monotonicity Test

A valid alpha signal must show a near-monotonic increase in average returns from Q1 to Q5, not just a top-minus-bottom spread.

### Hit Rate Analysis

Hit rate (fraction of profitable trades) and profit factor (gross profit / gross loss) are computed separately for long and short legs.

### Turnover Decomposition

Signal turnover is decomposed into the contribution from rank changes within each quintile versus migrations across quintile boundaries.

## Residual Analysis

After controlling for systematic factors, the residual (idiosyncratic) return attribution must remain statistically significant (t-stat > 2.5).

### Statistical Significance

We require a minimum t-statistic of 2.5 on the IC across the full backtest period before a signal is permitted to proceed to out-of-sample testing.

### Multiple Testing Correction

Benjamini-Hochberg False Discovery Rate correction is applied when evaluating a batch of signals to control the expected proportion of false discoveries.

