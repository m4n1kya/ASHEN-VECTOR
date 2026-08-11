"""
Target generation logic for ASHEN-VECTOR.

Contains functions to generate target variables for predictive models.
"""

import pandas as pd
import numpy as np


def future_return(close: pd.Series, periods: int) -> pd.Series:
    """
    Computes the future return over a specified number of periods.
    
    The target aligned to time t represents the return from t to t + periods.
    
    Args:
        close (pd.Series): The close price series.
        periods (int): The number of periods into the future.
        
    Returns:
        pd.Series: The future return series.
    """
    return (close.shift(-periods) / close) - 1


def future_direction(close: pd.Series, periods: int) -> pd.Series:
    """
    Computes the future direction (1 for positive return, 0 for negative/zero return).
    
    The target aligned to time t represents the direction from t to t + periods.
    
    Args:
        close (pd.Series): The close price series.
        periods (int): The number of periods into the future.
        
    Returns:
        pd.Series: A series containing 1 if future_return > 0, 0 otherwise. 
                   NaNs are preserved.
    """
    fut_ret = future_return(close, periods)
    
    # We use np.where but keep NaNs as NaNs
    direction = pd.Series(np.where(fut_ret > 0, 1.0, 0.0), index=close.index)
    
    # Preserve NaNs from the future return calculation
    direction.loc[fut_ret.isna()] = np.nan
    
    return direction
