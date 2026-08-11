"""
Feature registry for ASHEN-VECTOR.

Maintains metadata about available features, their categories, lookback periods, 
and whether they use future data (to prevent look-ahead bias).
"""

from dataclasses import dataclass


@dataclass
class FeatureMetadata:
    """
    Metadata for a single feature.
    
    Attributes:
        name (str): The name of the feature.
        category (str): The category of the feature.
        description (str): A brief description of what the feature measures.
        lookback (int): The number of periods of historical data required to compute the feature.
        uses_future_data (bool): Whether the feature uses future data. Default is False.
    """
    name: str
    category: str
    description: str
    lookback: int
    uses_future_data: bool = False


# A comprehensive standard set of features
FEATURE_REGISTRY: dict[str, FeatureMetadata] = {
    "return_1d": FeatureMetadata("return_1d", "momentum", "1-day price return", 1, False),
    "return_5d": FeatureMetadata("return_5d", "momentum", "5-day price return", 5, False),
    "momentum_10": FeatureMetadata("momentum_10", "momentum", "10-day price momentum", 10, False),
    "sma_20": FeatureMetadata("sma_20", "trend", "20-day Simple Moving Average", 20, False),
    "ema_20": FeatureMetadata("ema_20", "trend", "20-day Exponential Moving Average", 20, False),
    "close_to_sma20": FeatureMetadata("close_to_sma20", "trend", "Ratio of close price to 20-day SMA", 20, False),
    "volatility_20": FeatureMetadata("volatility_20", "volatility", "20-day annualized volatility", 20, False),
    "atr": FeatureMetadata("atr", "volatility", "Average True Range", 14, False),
    "rsi_14": FeatureMetadata("rsi_14", "momentum", "14-day Relative Strength Index", 14, False),
    "macd": FeatureMetadata("macd", "trend", "Moving Average Convergence Divergence", 26, False),
    "macd_signal": FeatureMetadata("macd_signal", "trend", "MACD Signal Line", 34, False),
    "macd_histogram": FeatureMetadata("macd_histogram", "trend", "MACD Histogram", 34, False),
    "bb_upper": FeatureMetadata("bb_upper", "volatility", "Bollinger Bands Upper Band", 20, False),
    "bb_lower": FeatureMetadata("bb_lower", "volatility", "Bollinger Bands Lower Band", 20, False),
    "bb_middle": FeatureMetadata("bb_middle", "volatility", "Bollinger Bands Middle Band (SMA)", 20, False),
    "bb_width": FeatureMetadata("bb_width", "volatility", "Bollinger Bands Width", 20, False),
    "bb_position": FeatureMetadata("bb_position", "volatility", "Close price position within Bollinger Bands", 20, False),
    "volume_change_1d": FeatureMetadata("volume_change_1d", "volume", "1-day volume change", 1, False),
    "volume_sma_20": FeatureMetadata("volume_sma_20", "volume", "20-day Volume SMA", 20, False),
    "volume_ratio_20": FeatureMetadata("volume_ratio_20", "volume", "Ratio of current volume to 20-day Volume SMA", 20, False),
    "high_low_range": FeatureMetadata("high_low_range", "volatility", "Intraday high-low range", 1, False),
    "open_close_range": FeatureMetadata("open_close_range", "volatility", "Intraday open-close range", 1, False),
}
