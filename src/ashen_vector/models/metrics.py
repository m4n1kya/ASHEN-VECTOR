"""
Metrics calculation for ML models and trading strategies.
"""
from typing import Dict, Any
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, log_loss, brier_score_loss, confusion_matrix,
    mean_absolute_error, mean_squared_error, r2_score
)

def classification_metrics(y_true: pd.Series, y_prob: pd.Series) -> Dict[str, Any]:
    """Calculate classification metrics."""
    y_pred = (y_prob > 0.5).astype(int)
    
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
    }
    
    try:
        metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob))
        metrics["log_loss"] = float(log_loss(y_true, y_prob))
        metrics["brier_score"] = float(brier_score_loss(y_true, y_prob))
    except Exception:
        pass
        
    return metrics

def regression_metrics(y_true: pd.Series, y_pred: pd.Series) -> Dict[str, Any]:
    """Calculate regression metrics."""
    metrics = {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }
    
    # Information Coefficient (Rank Correlation)
    ic = y_true.corr(y_pred, method='spearman')
    metrics["ic"] = float(ic) if pd.notna(ic) else 0.0
    
    # Directional Accuracy
    dir_true = np.sign(y_true)
    dir_pred = np.sign(y_pred)
    dir_acc = (dir_true == dir_pred).mean()
    metrics["directional_accuracy"] = float(dir_acc)
    
    return metrics
