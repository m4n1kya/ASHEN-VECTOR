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

## Walk-Forward Optimization

Hyperparameters are optimized exclusively on in-sample data within each rolling window, then applied identically to the subsequent out-of-sample period.

### Sample Splitting

The backtest is structurally divided into 70% in-sample (training) and 30% out-of-sample (validation), with a 6-month embargo buffer between them.

## Regime-Conditional Backtesting

Backtest performance is decomposed by market regime (BULL, BEAR, HIGH VOL, LOW VOL) to assess strategy robustness across all conditions.

### Historical Stress Tests

All strategies are stress-tested against the GFC (2008-09), COVID crash (2020-03), and 2022 rate-hike drawdown periods as mandatory validation gates.

### Expected Shortfall (CVaR)

Expected Shortfall at the 5% confidence level is computed across the full return distribution, providing a more complete tail risk picture than simple VaR.

### Drawdown Analysis

Drawdown analysis decomposes maximum drawdown into duration, recovery time, and the spread between underwater and recovery periods.

### Treynor Ratio

The Treynor Ratio normalizes excess returns by the portfolio's systematic beta, isolating the compensation received for taking market risk.

### Sortino Ratio

The Sortino Ratio is used alongside Sharpe to penalize only downside volatility, which is economically more relevant than symmetric volatility.

### Calmar Ratio

The Calmar Ratio (CAGR / Maximum Drawdown) is a primary ranking metric for comparing strategies with similar Sharpe Ratios but different risk profiles.

### Omega Ratio

The Omega Ratio evaluates the complete empirical return distribution, measuring the probability-weighted ratio of gains to losses above a minimum threshold.

### Distributional Constraints

Strategies with significant negative skewness (below -1.0) are rejected regardless of Sharpe Ratio, as they tend to exhibit catastrophic left-tail losses.

## Signal Combination

Multiple orthogonal signals are combined using an inverse-IC-variance weighting scheme, giving more weight to signals with historically stable information content.

### ML-Based Weighting

A secondary XGBoost model is trained to predict the IC of each signal conditional on the current market regime, enabling dynamic signal weight allocation.

### Equal-Weight Baseline

All ML-based combination schemes are benchmarked against a naive equal-weight combination to ensure the model complexity is justified.

### PCA Signal Compression

Principal Component Analysis extracts orthogonal composite signals from a large library of correlated raw signals, reducing noise and improving stability.

## Research Reproducibility

All research notebooks are versioned in Git with pinned `requirements.txt` and a fixed random seed, ensuring any analyst can reproduce results identically.

### Data Version Control

DVC tracks every dataset used in a research notebook, storing a content hash that allows exact historical datasets to be recreated on demand.

### MLflow Experiment Tracking

Every research experiment logs its parameters, metrics, and artifacts to MLflow, creating a permanent, searchable record of all historical research.

### Peer Review Gate

No signal may be promoted to the paper trading portfolio without a mandatory peer review from a second quantitative researcher.

## Paper Trading Validation

All approved signals must undergo a minimum 90-day paper trading period before live capital allocation, validating performance out-of-sample in real-time.

### Live vs. Backtest Reconciliation

A formal reconciliation is run monthly comparing live paper trading performance to the corresponding backtest period to detect implementation errors.

## Performance Attribution

Realized portfolio returns are decomposed using the Brinson-Hood-Beebower model into allocation effect, selection effect, and interaction effect.

### Factor Attribution

Barra-style factor attribution decomposes realized alpha into contributions from each systematic risk factor and the true residual idiosyncratic return.

### Sector vs. Stock Attribution

The attribution framework cleanly separates returns derived from overweighting a sector (allocation) from returns from picking winners within it (selection).

### Timing vs. Sizing

Attribution is further decomposed into the value added by the signal's ability to time entries versus its ability to size positions appropriately.

### Cost Attribution

Transaction costs are attributed separately to market impact, bid-ask spread crossing, and exchange fees to identify the most expensive rebalances.

## Benchmark Construction

Custom benchmarks are constructed from the investable universe itself to avoid the distortion caused by comparing against capitalization-weighted indices.

### Fundamental Law of Active Management

Grinold's Fundamental Law (IR ~ IC * sqrt(Breadth)) is used to estimate the theoretical maximum IR achievable given the signal quality and trading frequency.

### Transfer Coefficient

The Transfer Coefficient measures how faithfully portfolio weights reflect signal rankings after applying all constraints; a TC below 0.6 indicates severe constraint drag.

## Signal Construction Paradigms

Cross-sectional signals rank instruments against each other at each point in time, while time-series signals evaluate each instrument against its own history.

### Hybrid Signals

The most powerful signals are often hybrid constructions: selecting instruments that score well cross-sectionally AND are in a positive time-series trend.

### Volatility Adjustment

All cross-sectional ranks are adjusted for trailing realized volatility, preventing high-vol stocks from dominating the return distribution due to noise.

## Factor Exposure Management

Rolling factor exposures of the live portfolio are monitored daily. Breaching the +/-0.3 exposure limit on any Barra factor triggers a forced rebalance.

### Beta Neutrality

The optimizer enforces a maximum net market beta of +/-0.1, ensuring the strategy P&L is driven by stock selection rather than directional market exposure.

### Dollar Neutrality

For market-neutral strategies, gross long exposure equals gross short exposure within a +/-2% tolerance band, enforced at every rebalancing cycle.

### FX and Country Exposure

For multi-regional strategies, net currency exposure to any single non-USD currency is capped at 10% of NAV and hedged via FX forwards.

## Liquidity-Adjusted Sizing

Maximum position sizes are dynamically capped based on the instrument ADTV, ensuring no single position requires more than 3 days of volume to exit.

### Almgren-Chriss Impact Model

The Almgren-Chriss model estimates the expected market impact of executing a target position, directly feeding into the portfolio optimizer cost function.

### Volatility Targeting

Position sizes are scaled inversely to the GARCH-forecasted realized volatility, maintaining a consistent risk contribution across all holdings.

## Correlation Dynamics

During crisis periods, cross-asset correlations spike toward 1.0, destroying diversification benefits. The system detects this regime shift and reduces gross exposure.

### DCC-GARCH Model

Dynamic Conditional Correlation GARCH (DCC-GARCH) provides time-varying correlation estimates, capturing the rapid correlation spikes during market dislocations.

## Signal Deprecation

Signals that show a statistically significant IC decay over any trailing 12-month period are flagged for review and potentially sunset from the live portfolio.

### Decay Rate Monitoring

An exponentially smoothed ICIR is tracked for every live signal. If it falls below 0.3 for 4 consecutive weeks, the signal is automatically de-weighted.

### Regime-Switching Detection

HMM-based regime classifiers detect when a signal switches from momentum-driven to reversion-driven behavior, triggering a sign-flip adjustment.

## Alternative Data Due Diligence

Every alternative data vendor undergoes a rigorous legal, compliance, and statistical review before their data is integrated into the research pipeline.

### Legal Review

The legal review validates that the data was collected ethically, does not constitute material non-public information (MNPI), and complies with all data licensing terms.

### Statistical Power Analysis

Before purchasing a dataset, a power analysis estimates the minimum detectable IC given the dataset coverage and sample size, filtering out underpowered datasets.

## Pairs Trading

The pairs trading module identifies statistically cointegrated stock pairs using the Engle-Granger two-step procedure and the Johansen cointegration test.

### Spread Z-Score

The normalized spread between cointegrated pairs is z-scored using a rolling 252-day window; entries are triggered at +/-2 sigma and exits at mean reversion.

### Cointegration Stability

The cointegration relationship is re-tested quarterly. If the p-value of the ADF test exceeds 0.05, the pair is automatically dissolved from the portfolio.

## Implied Information Signals

Options market data provides forward-looking signals unavailable in price history: implied volatility surface, skew, and put/call volume ratios.

### IV Term Structure

The slope of the implied volatility term structure (30D vs 90D IV) predicts near-term event risk and is used as an input to the GARCH volatility forecast.

### Volatility Risk Premium

The Volatility Risk Premium (realized vol minus implied vol) is a robust cross-sectional signal; stocks with high VRP tend to deliver excess returns.

### Options Skew

Negative options skew (put IV greater than call IV) indicates the market is pricing tail risk; extreme skew paired with low realized vol signals a volatility compression trade.

### Post-Earnings Announcement Drift

Post-Earnings Announcement Drift (PEAD) exploits the documented underreaction to earnings surprises, going long on positive and short on negative surprises.

### SUE Score

Standardized Unexpected Earnings (SUE) normalizes the earnings surprise by its trailing standard deviation, making it comparable across companies of different sizes.

### Overnight Return Anomaly

The overnight return anomaly (close-to-open) is a well-documented microstructure phenomenon exploited via limit orders placed at the MOC auction.

### Seasonal Signals

Day-of-week and month-of-year seasonality patterns are catalogued but applied only to portfolio overlay timing, not as primary alpha signals.

### Tax-Loss Selling

Year-end tax-loss selling pressure creates a predictable January Effect bounce in prior-year losers; this is exploited as a mean-reversion signal.

### Index Reconstitution

Additions to major indices (S&P 500, Russell 2000) create predictable demand pressure. The strategy front-runs the reconstitution-day buying.

### Short Squeeze Detection

Short squeeze candidates are identified by crossing high short interest ratio (above 20%) with rapidly accelerating price momentum and increasing borrow rate.

## Crowding Risk

Crowding risk measures the degree to which our positions overlap with other institutional hedge fund books, creating vulnerability to simultaneous de-risking.

### 13F Analysis

Quarterly SEC 13F filings are aggregated to construct a Hedge Fund Crowding Index, penalizing stocks that appear in the top 10 holdings of more than 30 funds.

### Borrow Rate Monitoring

Short positions with stock borrow costs exceeding 500bps annually are flagged, as the carry cost can erase the alpha within the holding period.

