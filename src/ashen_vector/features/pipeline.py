"""
Feature pipeline for ASHEN-VECTOR.

Responsible for orchestrating technical indicators to generate the final feature set,
handling data warm-up periods, and ensuring targets are separated from features.
"""

import pandas as pd
import numpy as np
from datetime import timedelta

from ashen_vector.data.qlib_provider import QlibProvider
from ashen_vector.features import technical
from ashen_vector.features import targets


class FeaturePipeline:
    """Orchestrates feature generation and training dataset construction."""

    def __init__(self, provider: QlibProvider):
        self.provider = provider
        if not self.provider.is_initialized():
            self.provider.initialize()

    def _fetch_with_warmup(self, symbol: str, start_date: str, end_date: str, max_lookback_days: int) -> pd.DataFrame:
        start_ts = pd.to_datetime(start_date)
        calendar_padding = int(max_lookback_days * 1.5) + 20
        warmup_start = start_ts - timedelta(days=calendar_padding)
        warmup_start_str = warmup_start.strftime("%Y-%m-%d")
        
        df = self.provider.get_history(symbol, start_date=warmup_start_str, end_date=end_date)
        return df

    def build_features(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        df = self._fetch_with_warmup(symbol, start_date, end_date, max_lookback_days=200)
        
        if df.empty:
            return df
            
        open_p = df["$open"]
        high_p = df["$high"]
        low_p = df["$low"]
        close_p = df["$close"]
        vol_p = df["$volume"]

        features = pd.DataFrame(index=df.index)
        
        features["return_1d"] = technical.simple_returns(close_p)
        features["return_2d"] = close_p.pct_change(2)
        features["return_5d"] = close_p.pct_change(5)
        features["return_10d"] = close_p.pct_change(10)
        features["return_20d"] = close_p.pct_change(20)
        
        features["log_return_1d"] = technical.log_returns(close_p)
        features["log_return_5d"] = np.log(close_p / close_p.shift(5))
        
        features["momentum_5"] = technical.momentum(close_p, period=5)
        features["momentum_10"] = technical.momentum(close_p, period=10)
        features["momentum_20"] = technical.momentum(close_p, period=20)
        features["momentum_60"] = technical.momentum(close_p, period=60)
        
        sma_5 = technical.sma(close_p, window=5)
        sma_10 = technical.sma(close_p, window=10)
        sma_20 = technical.sma(close_p, window=20)
        sma_50 = technical.sma(close_p, window=50)
        sma_100 = technical.sma(close_p, window=100)
        sma_200 = technical.sma(close_p, window=200)
        
        features["sma_5"] = sma_5
        features["sma_10"] = sma_10
        features["sma_20"] = sma_20
        features["sma_50"] = sma_50
        features["sma_100"] = sma_100
        features["sma_200"] = sma_200
        
        features["ema_5"] = technical.ema(close_p, span=5)
        features["ema_10"] = technical.ema(close_p, span=10)
        features["ema_20"] = technical.ema(close_p, span=20)
        features["ema_50"] = technical.ema(close_p, span=50)
        
        features["close_to_sma20"] = (close_p - sma_20) / sma_20.replace(0, np.nan)
        features["close_to_sma50"] = (close_p - sma_50) / sma_50.replace(0, np.nan)
        features["close_to_sma200"] = (close_p - sma_200) / sma_200.replace(0, np.nan)
        
        features["volatility_5"] = technical.rolling_volatility(features["return_1d"], window=5)
        features["volatility_10"] = technical.rolling_volatility(features["return_1d"], window=10)
        features["volatility_20"] = technical.rolling_volatility(features["return_1d"], window=20)
        features["volatility_60"] = technical.rolling_volatility(features["return_1d"], window=60)
        
        atr = technical.atr(high_p, low_p, close_p, period=14)
        features["atr"] = atr
        features["atr_pct"] = atr / close_p.replace(0, np.nan)
        
        features["rsi_14"] = technical.rsi(close_p, period=14)
        
        macd, macd_signal, macd_hist = technical.macd(close_p)
        features["macd"] = macd
        features["macd_signal"] = macd_signal
        features["macd_histogram"] = macd_hist
        
        bb_upper, bb_middle, bb_lower = technical.bollinger_bands(close_p, window=20)
        features["bb_middle"] = bb_middle
        features["bb_upper"] = bb_upper
        features["bb_lower"] = bb_lower
        features["bb_width"] = technical.bb_width(bb_upper, bb_middle, bb_lower)
        features["bb_position"] = technical.bb_position(close_p, bb_upper, bb_lower)
        
        features["volume_change_1d"] = vol_p.pct_change()
        features["volume_sma_5"] = technical.volume_sma(vol_p, window=5)
        features["volume_sma_20"] = technical.volume_sma(vol_p, window=20)
        features["volume_ratio_20"] = technical.volume_ratio(vol_p, window=20)
        
        features["high_low_range"] = technical.high_low_range(high_p, low_p, close_p)
        features["open_close_range"] = technical.open_close_range(open_p, close_p)
        features["close_to_high"] = technical.distance_from_high(close_p, window=200)
        features["close_to_low"] = technical.distance_from_low(close_p, window=200)
        
        features["return_1d_lag1"] = features["return_1d"].shift(1)
        features["return_1d_lag2"] = features["return_1d"].shift(2)
        features["return_1d_lag3"] = features["return_1d"].shift(3)
        features["return_1d_lag5"] = features["return_1d"].shift(5)
        
        features["volume_ratio_lag1"] = features["volume_ratio_20"].shift(1)
        features["rsi_lag1"] = features["rsi_14"].shift(1)
        features["volatility_lag1"] = features["volatility_20"].shift(1)

        start_ts = pd.to_datetime(start_date)
        end_ts = pd.to_datetime(end_date)
        
        features = features.loc[(features.index >= start_ts) & (features.index <= end_ts)].copy()
        features = features.replace([np.inf, -np.inf], np.nan)
        
        return features

    def get_feature_names(self) -> list[str]:
        """Return the explicit whitelist of features generated by the pipeline."""
        # This is a safe way to ensure we only get generated features without running fetch.
        # However, because we generate them dynamically, we can just run a dummy date
        # or statically define them. 
        # For safety and maintenance, let's keep it aligned.
        dummy_df = pd.DataFrame({
            "$open": [1, 2], "$high": [2, 3], "$low": [1, 1], "$close": [2, 3], "$volume": [100, 200]
        }, index=pd.date_range("2000-01-01", periods=2))
        
        # We can extract the columns by creating a dummy DataFrame that matches our logic, 
        # or simply list them explicitly to guarantee no targets can ever slip in.
        return [
            "return_1d", "return_2d", "return_5d", "return_10d", "return_20d",
            "log_return_1d", "log_return_5d",
            "momentum_5", "momentum_10", "momentum_20", "momentum_60",
            "sma_5", "sma_10", "sma_20", "sma_50", "sma_100", "sma_200",
            "ema_5", "ema_10", "ema_20", "ema_50",
            "close_to_sma20", "close_to_sma50", "close_to_sma200",
            "volatility_5", "volatility_10", "volatility_20", "volatility_60",
            "atr", "atr_pct", "rsi_14", 
            "macd", "macd_signal", "macd_histogram",
            "bb_middle", "bb_upper", "bb_lower", "bb_width", "bb_position",
            "volume_change_1d", "volume_sma_5", "volume_sma_20", "volume_ratio_20",
            "high_low_range", "open_close_range", "close_to_high", "close_to_low",
            "return_1d_lag1", "return_1d_lag2", "return_1d_lag3", "return_1d_lag5",
            "volume_ratio_lag1", "rsi_lag1", "volatility_lag1"
        ]

    def build_training_dataset(self, symbol: str, start_date: str, end_date: str) -> tuple[pd.DataFrame, pd.DataFrame]:
        max_target_horizon = 20
        calendar_padding = int(max_target_horizon * 1.5) + 10
        end_ts = pd.to_datetime(end_date)
        target_end_str = (end_ts + timedelta(days=calendar_padding)).strftime("%Y-%m-%d")
        
        raw_df = self._fetch_with_warmup(symbol, start_date, target_end_str, max_lookback_days=200)
        
        if raw_df.empty:
            return pd.DataFrame(), pd.DataFrame()
            
        close_p = raw_df["$close"]
        
        y = pd.DataFrame(index=raw_df.index)
        y["future_return_1d"] = targets.future_return(close_p, periods=1)
        y["future_return_5d"] = targets.future_return(close_p, periods=5)
        y["future_return_10d"] = targets.future_return(close_p, periods=10)
        y["future_return_20d"] = targets.future_return(close_p, periods=20)
        
        y["direction_1d"] = targets.future_direction(close_p, periods=1)
        y["direction_5d"] = targets.future_direction(close_p, periods=5)
        y["direction_10d"] = targets.future_direction(close_p, periods=10)
        y["direction_20d"] = targets.future_direction(close_p, periods=20)
        
        start_ts = pd.to_datetime(start_date)
        y = y.loc[(y.index >= start_ts) & (y.index <= end_ts)].copy()
        
        X = self.build_features(symbol, start_date, end_date)
        
        X, y = X.align(y, join="inner", axis=0)
        assert set(X.columns).isdisjoint(set(y.columns)), "CRITICAL: Target column leaked into feature matrix!"
        
        return X, y
