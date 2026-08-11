"""
Metrics calculation for backtests.
Strictly separates predictive performance, trading performance, and risk metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, brier_score_loss

def calculate_drawdown_durations(equity_curve: pd.DataFrame) -> Dict[str, int]:
    """Calculates max, average, and current drawdown duration in trading days."""
    if equity_curve.empty or "drawdown" not in equity_curve.columns:
        return {"max_drawdown_duration_days": 0, "average_drawdown_duration_days": 0, "current_drawdown_duration_days": 0}
        
    dd = equity_curve["drawdown"] < 0
    
    # Calculate durations of contiguous True blocks
    durations = []
    current_duration = 0
    
    for is_dd in dd:
        if is_dd:
            current_duration += 1
        else:
            if current_duration > 0:
                durations.append(current_duration)
            current_duration = 0
            
    # The last one might still be ongoing
    current_dd = current_duration
    if current_duration > 0:
        durations.append(current_duration)
        
    return {
        "max_drawdown_duration_days": max(durations) if durations else 0,
        "average_drawdown_duration_days": int(np.mean(durations)) if durations else 0,
        "current_drawdown_duration_days": current_dd
    }

def calculate_predictive_metrics(predictions: pd.DataFrame) -> Dict[str, float]:
    """Calculates ML model predictive performance."""
    if predictions.empty:
        return {}
        
    mets = {}
    
    # Classification
    y_true_cls = predictions["actual_direction"]
    y_pred_prob = predictions["probability_up"]
    y_pred_cls = (y_pred_prob > 0.5).astype(int)
    
    mets["accuracy"] = float(accuracy_score(y_true_cls, y_pred_cls))
    mets["precision"] = float(precision_score(y_true_cls, y_pred_cls, zero_division=0))
    mets["recall"] = float(recall_score(y_true_cls, y_pred_cls, zero_division=0))
    mets["f1"] = float(f1_score(y_true_cls, y_pred_cls, zero_division=0))
    
    try:
        mets["roc_auc"] = float(roc_auc_score(y_true_cls, y_pred_prob))
        mets["brier_score"] = float(brier_score_loss(y_true_cls, y_pred_prob))
    except ValueError:
        pass
        
    # Regression
    y_true_reg = predictions["actual_return"]
    y_pred_reg = predictions["expected_return"]
    
    mets["correlation"] = float(y_true_reg.corr(y_pred_reg))
    
    return mets

def calculate_trading_metrics(equity_curve: pd.DataFrame) -> Dict[str, float]:
    """Calculates financial trading performance."""
    if equity_curve.empty:
        return {}
        
    mets = {}
    
    total_ret = equity_curve["cumulative_return"].iloc[-1]
    mets["cumulative_return"] = float(total_ret)
    
    # Annualized return (assuming 252 trading days)
    days = len(equity_curve)
    if days > 0:
        years = days / 252.0
        mets["annualized_return"] = float((1 + total_ret) ** (1 / years) - 1) if years > 0 else 0.0
    else:
        mets["annualized_return"] = 0.0
        
    # Trades and Win Rate
    # A trade occurs when position changes
    pos = equity_curve["position"]
    pos_diff = pos.diff().fillna(0)
    trades = pos_diff[pos_diff != 0]
    
    mets["number_of_trades"] = int(len(trades))
    
    # Approximating win rate from daily returns while holding
    holding_days = equity_curve[equity_curve["position"] != 0]
    if len(holding_days) > 0:
        winning_days = len(holding_days[holding_days["daily_return"] > 0])
        mets["win_rate"] = float(winning_days / len(holding_days))
    else:
        mets["win_rate"] = 0.0
        
    return mets

def calculate_risk_metrics(equity_curve: pd.DataFrame) -> Dict[str, Any]:
    """Calculates risk and drawdown metrics."""
    if equity_curve.empty:
        return {}
        
    mets = {}
    
    daily_rets = equity_curve["daily_return"]
    
    # Volatility
    ann_vol = daily_rets.std() * np.sqrt(252)
    mets["annualized_volatility"] = float(ann_vol)
    
    # Sharpe (assuming 0 risk-free rate)
    if ann_vol > 0:
        mets["sharpe_ratio"] = float((daily_rets.mean() * 252) / ann_vol)
    else:
        mets["sharpe_ratio"] = 0.0
        
    # Drawdown
    mets["max_drawdown"] = float(equity_curve["drawdown"].min())
    
    # Drawdown durations
    dd_durations = calculate_drawdown_durations(equity_curve)
    mets.update(dd_durations)
    
    return mets

def generate_model_verdict(model_metrics: Dict, baseline_metrics: Dict) -> str:
    """Generate VERDICT compared to Buy & Hold."""
    try:
        mod_ret = model_metrics["trading_performance"]["cumulative_return"]
        base_ret = baseline_metrics["trading_performance"]["cumulative_return"]
        
        mod_dd = model_metrics["risk_metrics"]["max_drawdown"]
        base_dd = baseline_metrics["risk_metrics"]["max_drawdown"]
        
        if mod_ret > base_ret and mod_dd > base_dd:  # max_drawdown is negative
            return "OUTPERFORMING"
        elif mod_ret < base_ret and mod_dd < base_dd:
            return "UNDERPERFORMING"
        else:
            return "COMPARABLE"
    except KeyError:
        return "INSUFFICIENT EVIDENCE"
