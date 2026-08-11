"""Technical indicator calculations for quantitative analysis.

All functions operate on pandas Series/DataFrames and are independent
of the data source. They can be used with Qlib data, CSV data, or any
other time-series source.

IMPORTANT: All indicators use only past and current data.
No future information is ever used in calculations.
"""

import pandas as pd
import numpy as np


def sma(series: pd.Series, window: int) -> pd.Series:
    """Simple Moving Average."""
    return series.rolling(window=window, min_periods=window).mean()


def ema(series: pd.Series, span: int) -> pd.Series:
    """Exponential Moving Average."""
    return series.ewm(span=span, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index (Wilder's method).
    
    Returns values between 0 and 100.
    """
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    
    avg_gain = gain.ewm(alpha=1.0/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0/period, min_periods=period, adjust=False).mean()
    
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100.0 - (100.0 / (1.0 + rs))


def macd(
    series: pd.Series,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """MACD (Moving Average Convergence Divergence).
    
    Returns:
        Tuple of (macd_line, signal_line, histogram)
    """
    fast_ema = ema(series, fast_period)
    slow_ema = ema(series, slow_period)
    macd_line = fast_ema - slow_ema
    signal_line = ema(macd_line, signal_period)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def bollinger_bands(
    series: pd.Series, window: int = 20, num_std: float = 2.0
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Bollinger Bands.
    
    Returns:
        Tuple of (upper_band, middle_band, lower_band)
    """
    middle = sma(series, window)
    std = series.rolling(window=window, min_periods=window).std()
    upper = middle + (std * num_std)
    lower = middle - (std * num_std)
    return upper, middle, lower


def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """Average True Range."""
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return true_range.rolling(window=period, min_periods=period).mean()


def rolling_volatility(returns: pd.Series, window: int = 20) -> pd.Series:
    """Rolling annualized volatility from returns."""
    return returns.rolling(window=window, min_periods=window).std() * np.sqrt(252)


def momentum(series: pd.Series, period: int = 10) -> pd.Series:
    """Price momentum (rate of change)."""
    return series / series.shift(period) - 1.0


def log_returns(series: pd.Series) -> pd.Series:
    """Logarithmic returns."""
    return np.log(series / series.shift(1))


def simple_returns(series: pd.Series) -> pd.Series:
    """Simple percentage returns."""
    return series.pct_change()


def volume_sma(volume: pd.Series, window: int = 20) -> pd.Series:
    """Volume simple moving average."""
    return sma(volume, window)


def volume_ratio(volume: pd.Series, window: int = 20) -> pd.Series:
    """Current volume relative to its moving average."""
    avg = volume_sma(volume, window)
    return volume / avg.replace(0, np.nan)


def price_to_sma_ratio(price: pd.Series, window: int) -> pd.Series:
    """Price relative to its simple moving average."""
    return price / sma(price, window)


def rolling_max(series: pd.Series, window: int) -> pd.Series:
    """Rolling maximum."""
    return series.rolling(window=window, min_periods=1).max()


def rolling_min(series: pd.Series, window: int) -> pd.Series:
    """Rolling minimum."""
    return series.rolling(window=window, min_periods=1).min()


def drawdown(series: pd.Series, window: int = 252) -> pd.Series:
    """Drawdown from rolling peak."""
    peak = rolling_max(series, window)
    return (series - peak) / peak


def distance_from_high(price: pd.Series, window: int = 252) -> pd.Series:
    """Percentage distance from rolling high."""
    high = rolling_max(price, window)
    return (price - high) / high


def distance_from_low(price: pd.Series, window: int = 252) -> pd.Series:
    """Percentage distance from rolling low."""
    low = rolling_min(price, window)
    return (price - low) / low.replace(0, np.nan)


def intraday_range(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    """Intraday range as a fraction of close price."""
    return (high - low) / close.replace(0, np.nan)


def gap(open_price: pd.Series, prev_close: pd.Series) -> pd.Series:
    """Overnight gap."""
    return (open_price - prev_close) / prev_close.replace(0, np.nan)


def bb_width(upper: pd.Series, middle: pd.Series, lower: pd.Series) -> pd.Series:
    """Bollinger Bands width."""
    return (upper - lower) / middle.replace(0, np.nan)


def bb_position(price: pd.Series, upper: pd.Series, lower: pd.Series) -> pd.Series:
    """Position of price within Bollinger Bands (0 = lower, 1 = upper)."""
    band_range = (upper - lower).replace(0, np.nan)
    return (price - lower) / band_range


def high_low_range(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    """High-low range as a fraction of close."""
    return (high - low) / close.replace(0, np.nan)


def open_close_range(open_price: pd.Series, close: pd.Series) -> pd.Series:
    """Open-close absolute range as a fraction of close."""
    return (close - open_price).abs() / close.replace(0, np.nan)
