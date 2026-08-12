import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, brier_score_loss, log_loss, confusion_matrix
)
from typing import Dict, Any, List

def calculate_predictive_metrics(y_true: pd.Series, y_prob: pd.Series, threshold=0.5) -> Dict[str, Any]:
    y_pred = (y_prob > threshold).astype(int)
    
    try:
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        
        # Some metrics require both classes
        if len(np.unique(y_true)) > 1:
            roc_auc = roc_auc_score(y_true, y_prob)
            logl = log_loss(y_true, y_prob)
            brier = brier_score_loss(y_true, y_prob)
        else:
            roc_auc, logl, brier = 0.5, 0.0, 0.0
            
        cm = confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist()
        
    except Exception as e:
        acc, prec, rec, f1, roc_auc, logl, brier, cm = 0, 0, 0, 0, 0, 0, 0, [[0,0],[0,0]]
        
    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "roc_auc": roc_auc,
        "log_loss": logl,
        "brier_score": brier,
        "confusion_matrix": cm
    }

def calculate_calibration(y_true: pd.Series, y_prob: pd.Series, n_bins=10) -> Dict[str, Any]:
    bins = np.linspace(0, 1, n_bins + 1)
    indices = np.digitize(y_prob, bins) - 1
    
    curve = []
    for i in range(n_bins):
        mask = (indices == i)
        if mask.sum() > 0:
            prob_mean = y_prob[mask].mean()
            obs_freq = y_true[mask].mean()
            count = int(mask.sum())
            curve.append({
                "bucket": f"{int(bins[i]*100)}-{int(bins[i+1]*100)}%",
                "predicted": float(prob_mean),
                "observed": float(obs_freq),
                "count": count
            })
    return {"curve": curve}

def calculate_trading_metrics(returns: pd.Series, benchmark_returns: pd.Series = None) -> Dict[str, Any]:
    returns = returns.fillna(0)
    if len(returns) == 0:
        return {}
        
    cum_returns = (1 + returns).cumprod()
    total_return = cum_returns.iloc[-1] - 1
    
    ann_factor = 252
    ann_return = (1 + total_return) ** (ann_factor / len(returns)) - 1
    ann_vol = returns.std() * np.sqrt(ann_factor)
    
    sharpe = ann_return / ann_vol if ann_vol > 0 else 0
    
    neg_returns = returns[returns < 0]
    sortino = ann_return / (neg_returns.std() * np.sqrt(ann_factor)) if len(neg_returns) > 0 and neg_returns.std() > 0 else 0
    
    rolling_max = cum_returns.cummax()
    drawdown = (cum_returns - rolling_max) / rolling_max
    max_dd = drawdown.min()
    
    calmar = ann_return / abs(max_dd) if max_dd < 0 else 0
    
    win_rate = (returns > 0).mean()
    gross_profit = returns[returns > 0].sum()
    gross_loss = abs(returns[returns < 0].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
    
    return {
        "cumulative_return": float(total_return),
        "annualized_return": float(ann_return),
        "annualized_volatility": float(ann_vol),
        "sharpe_ratio": float(sharpe),
        "sortino_ratio": float(sortino),
        "calmar_ratio": float(calmar),
        "max_drawdown": float(max_dd),
        "win_rate": float(win_rate),
        "profit_factor": float(profit_factor),
        "num_trades": len(returns[returns != 0])
    }

def calculate_verdict(sharpe: float, return_val: float, benchmark_return: float) -> str:
    if sharpe > 1.0 and return_val > benchmark_return:
        return "OUTPERFORMING"
    elif sharpe > 0.5 and return_val > 0:
        return "COMPARABLE"
    else:
        return "UNDERPERFORMING"
