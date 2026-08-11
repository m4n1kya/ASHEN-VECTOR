"""
Naive baselines for predictive modeling and trading strategies.
Used for performance gating and model evaluation.
"""

import numpy as np
import pandas as pd
from typing import Dict


class PredictiveBaselines:
    """Predictive baseline models for comparison."""
    
    @staticmethod
    def majority_class(y_train: pd.Series, y_test: pd.Series) -> pd.Series:
        """Predicts the most common class from the training set."""
        majority_val = y_train.mode()[0]
        return pd.Series(majority_val, index=y_test.index)
        
    @staticmethod
    def random_classifier(y_test: pd.Series, p_positive: float = 0.5) -> pd.Series:
        """Predicts randomly based on a given probability."""
        np.random.seed(42)
        preds = (np.random.rand(len(y_test)) < p_positive).astype(int)
        return pd.Series(preds, index=y_test.index)
        
    @staticmethod
    def previous_return(X_test: pd.DataFrame, return_col: str = "return_1d") -> pd.Series:
        """Predicts the future return is identical to the most recent return."""
        if return_col in X_test.columns:
            return X_test[return_col]
        return pd.Series(0.0, index=X_test.index)


class TradingBaselines:
    """Trading strategy baselines for risk-adjusted performance comparison."""
    
    @staticmethod
    def buy_and_hold(prices: pd.Series) -> pd.Series:
        """Generates continuous 'BUY' (1) signals."""
        return pd.Series(1.0, index=prices.index)
        
    @staticmethod
    def moving_average_crossover(prices: pd.Series, short_window: int = 20, long_window: int = 50) -> pd.Series:
        """Standard MA crossover strategy. 1 if short > long, 0 otherwise."""
        short_ma = prices.rolling(window=short_window, min_periods=1).mean()
        long_ma = prices.rolling(window=long_window, min_periods=1).mean()
        signal = (short_ma > long_ma).astype(float)
        return signal
        
    @staticmethod
    def momentum(prices: pd.Series, window: int = 10) -> pd.Series:
        """Momentum strategy. 1 if current price > price `window` days ago."""
        past_price = prices.shift(window)
        # Avoid dividing by 0 or NaNs by just checking >
        signal = (prices > past_price).astype(float)
        # Handle initial window NaNs
        signal.iloc[:window] = 0.0
        return signal
