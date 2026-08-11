"""
Benchmarks for backtesting evaluation.
Generates target positions for baseline strategies.
"""

import pandas as pd
import numpy as np
from ashen_vector.features.technical import sma, momentum

class Benchmarks:
    """Generates signals for standard financial benchmarks."""
    
    @staticmethod
    def buy_and_hold(prices: pd.Series) -> pd.Series:
        """Always holds 100% of the asset."""
        return pd.Series(1.0, index=prices.index, name="target_position")
        
    @staticmethod
    def sma_crossover(prices: pd.Series, window: int = 20) -> pd.Series:
        """Long when price is above SMA, flat when below."""
        sma_vals = sma(prices, window=window)
        
        signals = pd.Series(0.0, index=prices.index, name="target_position")
        signals.loc[prices > sma_vals] = 1.0
        return signals
        
    @staticmethod
    def momentum_strategy(prices: pd.Series, period: int = 20) -> pd.Series:
        """Long when momentum is positive, flat when negative."""
        mom = momentum(prices, period=period)
        
        signals = pd.Series(0.0, index=prices.index, name="target_position")
        signals.loc[mom > 0] = 1.0
        return signals
