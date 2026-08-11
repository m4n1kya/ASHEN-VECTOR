"""Financial statistics calculations.

Computes standard quantitative statistics from historical price data.
All calculations use only available historical data — never fabricated values.
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Optional


@dataclass
class PriceStatistics:
    """Summary statistics for an instrument's price history."""
    symbol: str
    latest_date: str
    latest_close: float
    daily_return: Optional[float]
    weekly_return: Optional[float]  # 5-day
    monthly_return: Optional[float]  # 21-day
    total_return: Optional[float]
    annualized_return: Optional[float]
    volatility_daily: Optional[float]
    volatility_annualized: Optional[float]
    max_drawdown: Optional[float]
    sharpe_ratio: Optional[float]  # Assuming 0 risk-free rate
    sortino_ratio: Optional[float]
    win_rate: Optional[float]
    avg_positive_return: Optional[float]
    avg_negative_return: Optional[float]
    best_day: Optional[float]
    worst_day: Optional[float]
    high_52w: Optional[float]
    low_52w: Optional[float]
    distance_from_52w_high: Optional[float]
    distance_from_52w_low: Optional[float]
    total_trading_days: int


def compute_statistics(close: pd.Series, symbol: str = "UNKNOWN") -> PriceStatistics:
    """Compute comprehensive price statistics from a close price series.
    
    Args:
        close: Time-indexed Series of close prices.
        symbol: Instrument symbol for labeling.
        
    Returns:
        PriceStatistics dataclass with computed values.
        Fields that cannot be computed from available data are set to None.
    """
    if close.empty:
        return PriceStatistics(
            symbol=symbol,
            latest_date="N/A",
            latest_close=0.0,
            daily_return=None,
            weekly_return=None,
            monthly_return=None,
            total_return=None,
            annualized_return=None,
            volatility_daily=None,
            volatility_annualized=None,
            max_drawdown=None,
            sharpe_ratio=None,
            sortino_ratio=None,
            win_rate=None,
            avg_positive_return=None,
            avg_negative_return=None,
            best_day=None,
            worst_day=None,
            high_52w=None,
            low_52w=None,
            distance_from_52w_high=None,
            distance_from_52w_low=None,
            total_trading_days=0,
        )

    returns = close.pct_change().dropna()
    n_days = len(close)
    
    latest_date_val = close.index[-1]
    if hasattr(latest_date_val, '__len__') and len(latest_date_val) == 2:
        latest_date_val = latest_date_val[1]  # MultiIndex from Qlib
    latest_date_str = str(latest_date_val.date()) if hasattr(latest_date_val, 'date') else str(latest_date_val)
    latest_close = float(close.iloc[-1])
    
    # Returns
    daily_ret = float(returns.iloc[-1]) if len(returns) >= 1 else None
    weekly_ret = float(close.iloc[-1] / close.iloc[-5] - 1) if n_days >= 5 else None
    monthly_ret = float(close.iloc[-1] / close.iloc[-21] - 1) if n_days >= 21 else None
    total_ret = float(close.iloc[-1] / close.iloc[0] - 1)
    
    # Annualized return
    ann_ret = None
    if n_days > 1:
        years = n_days / 252.0
        if years > 0 and close.iloc[0] > 0:
            ann_ret = float((close.iloc[-1] / close.iloc[0]) ** (1.0 / years) - 1)
    
    # Volatility
    vol_daily = float(returns.std()) if len(returns) > 1 else None
    vol_annual = vol_daily * np.sqrt(252) if vol_daily is not None else None
    
    # Drawdown
    cummax = close.cummax()
    dd = (close - cummax) / cummax
    max_dd = float(dd.min()) if len(dd) > 0 else None
    
    # Sharpe (assuming 0 risk-free rate)
    sharpe = None
    if vol_annual and vol_annual > 0 and ann_ret is not None:
        sharpe = float(ann_ret / vol_annual)
    
    # Sortino
    sortino = None
    negative_returns = returns[returns < 0]
    if len(negative_returns) > 1 and ann_ret is not None:
        downside_std = float(negative_returns.std()) * np.sqrt(252)
        if downside_std > 0:
            sortino = float(ann_ret / downside_std)
    
    # Win rate
    win_rate_val = float((returns > 0).sum() / len(returns)) if len(returns) > 0 else None
    
    # Average returns
    positive = returns[returns > 0]
    negative = returns[returns < 0]
    avg_pos = float(positive.mean()) if len(positive) > 0 else None
    avg_neg = float(negative.mean()) if len(negative) > 0 else None
    
    # Best/worst
    best = float(returns.max()) if len(returns) > 0 else None
    worst = float(returns.min()) if len(returns) > 0 else None
    
    # 52-week (252 trading days) high/low
    if n_days >= 252:
        recent = close.iloc[-252:]
    else:
        recent = close
    h52 = float(recent.max())
    l52 = float(recent.min())
    dist_high = float((latest_close - h52) / h52) if h52 > 0 else None
    dist_low = float((latest_close - l52) / l52) if l52 > 0 else None
    
    return PriceStatistics(
        symbol=symbol,
        latest_date=latest_date_str,
        latest_close=latest_close,
        daily_return=daily_ret,
        weekly_return=weekly_ret,
        monthly_return=monthly_ret,
        total_return=total_ret,
        annualized_return=ann_ret,
        volatility_daily=vol_daily,
        volatility_annualized=vol_annual,
        max_drawdown=max_dd,
        sharpe_ratio=sharpe,
        sortino_ratio=sortino,
        win_rate=win_rate_val,
        avg_positive_return=avg_pos,
        avg_negative_return=avg_neg,
        best_day=best,
        worst_day=worst,
        high_52w=h52,
        low_52w=l52,
        distance_from_52w_high=dist_high,
        distance_from_52w_low=dist_low,
        total_trading_days=n_days,
    )
