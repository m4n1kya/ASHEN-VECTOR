import numpy as np
import pandas as pd
import yfinance as yf
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import logging
from typing import Dict, Any, Tuple
import traceback
import time

from ashen_vector.models.validation import PurgedWalkForwardCV
from ashen_vector.api.services.validation_metrics import (
    calculate_predictive_metrics, calculate_calibration,
    calculate_trading_metrics, calculate_verdict
)

logger = logging.getLogger(__name__)

def generate_features(df: pd.DataFrame, horizon: int) -> pd.DataFrame:
    temp_df = df.copy()
    
    # 1. Targets (STRICTLY FOR TRAINING, REMOVED FOR INFERENCE)
    temp_df['future_return'] = (temp_df['Close'].shift(-horizon) / temp_df['Close'] - 1.0) / horizon
    temp_df['target_class'] = (temp_df['future_return'] > 0).astype(int)
    temp_df['target_reg'] = temp_df['future_return']
    
    # 2. Features (ONLY PAST DATA)
    temp_df['ret_1d'] = temp_df['Close'].pct_change()
    temp_df['sma_20'] = temp_df['Close'].rolling(20).mean() / temp_df['Close']
    temp_df['sma_50'] = temp_df['Close'].rolling(50).mean() / temp_df['Close']
    temp_df['vol_20'] = temp_df['ret_1d'].rolling(20).std()
    temp_df['mom_20'] = temp_df['Close'] / temp_df['Close'].shift(20) - 1.0
    
    # Drop rows with NaN due to rolling windows
    temp_df = temp_df.dropna(subset=['sma_50'])
    
    return temp_df

def run_validation_job(
    symbol: str,
    model_name: str,
    horizon: int,
    start_date: str = None,
    end_date: str = None,
    purge_window: int = 5,
    embargo_window: int = 5,
    n_splits: int = 5
) -> Dict[str, Any]:
    try:
        # 1. Fetch Data
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="10y")
        if df.empty:
            raise ValueError(f"No data found for {symbol}")
            
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
        df.index = df.index.tz_localize(None)
        
        # 2. Prepare Features & Targets
        df = generate_features(df, horizon)
        
        is_classification = not ("Regression" in model_name)
        target_col = 'target_class' if is_classification else 'target_reg'
        
        # Clean target NaNs (the last `horizon` days will have NaN target)
        df_trainable = df.dropna(subset=[target_col]).copy()
        
        features = ['ret_1d', 'sma_20', 'sma_50', 'vol_20', 'mom_20']
        
        # 3. Setup CV
        cv = PurgedWalkForwardCV(
            n_splits=n_splits,
            target_horizon=horizon,
            purge_window=purge_window,
            embargo_window=embargo_window,
            min_train_size=252 # At least 1 year of training data
        )
        
        all_oos_dates = []
        all_oos_y_true = []
        all_oos_y_prob = []
        all_oos_y_pred_reg = []
        
        fold_results = []
        feature_importances = []
        
        # 4. Walk-Forward Folds
        fold_idx = 1
        for train_idx, test_idx in cv.split(df_trainable):
            X_train = df_trainable.iloc[train_idx][features].values
            y_train = df_trainable.iloc[train_idx][target_col].values
            
            X_test = df_trainable.iloc[test_idx][features].values
            y_test = df_trainable.iloc[test_idx][target_col].values
            test_dates = df_trainable.iloc[test_idx].index
            
            # Model Selection
            if model_name == "LightGBM Classification":
                model = lgb.LGBMClassifier(n_estimators=100, max_depth=4, verbose=-1, random_state=42)
            elif model_name == "LightGBM Regression":
                model = lgb.LGBMRegressor(n_estimators=100, max_depth=4, verbose=-1, random_state=42)
            elif model_name == "Random Forest Classification":
                model = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=42)
            elif model_name == "Random Forest Regression":
                model = RandomForestRegressor(n_estimators=100, max_depth=4, random_state=42)
            else:
                model = lgb.LGBMClassifier(n_estimators=100, max_depth=4, verbose=-1, random_state=42)
                
            model.fit(X_train, y_train)
            
            # Predict
            if is_classification:
                y_prob = model.predict_proba(X_test)[:, 1]
                all_oos_y_prob.extend(y_prob)
                
                fold_acc = (y_test == (y_prob > 0.5)).mean()
                
                # Trading strategy: Go long if prob > 0.5, else cash
                fold_strategy_returns = df_trainable.iloc[test_idx]['future_return'] * (y_prob > 0.5)
            else:
                y_pred_reg = model.predict(X_test)
                all_oos_y_pred_reg.extend(y_pred_reg)
                
                fold_acc = np.corrcoef(y_test, y_pred_reg)[0, 1] if np.std(y_pred_reg) > 0 else 0
                
                # Trading strategy: Go long if pred return > 0
                fold_strategy_returns = df_trainable.iloc[test_idx]['future_return'] * (y_pred_reg > 0)
                
            all_oos_dates.extend(test_dates)
            all_oos_y_true.extend(y_test)
            
            # Fold metrics
            fold_sharpe = calculate_trading_metrics(fold_strategy_returns).get('sharpe_ratio', 0)
            fold_ret = calculate_trading_metrics(fold_strategy_returns).get('cumulative_return', 0)
            
            fold_results.append({
                "fold": fold_idx,
                "train_start": df_trainable.index[train_idx[0]].strftime("%Y-%m-%d"),
                "train_end": df_trainable.index[train_idx[-1]].strftime("%Y-%m-%d"),
                "test_start": df_trainable.index[test_idx[0]].strftime("%Y-%m-%d"),
                "test_end": df_trainable.index[test_idx[-1]].strftime("%Y-%m-%d"),
                "accuracy": float(fold_acc),
                "sharpe": float(fold_sharpe),
                "return": float(fold_ret)
            })
            
            if hasattr(model, 'feature_importances_'):
                feature_importances.append(model.feature_importances_)
                
            fold_idx += 1

        if len(all_oos_y_true) == 0:
            raise ValueError("Insufficient data to perform walk-forward validation.")
            
        # 5. Aggregate Global Metrics
        oos_dates = pd.DatetimeIndex(all_oos_dates)
        oos_true = pd.Series(all_oos_y_true, index=oos_dates)
        
        if is_classification:
            oos_prob = pd.Series(all_oos_y_prob, index=oos_dates)
            oos_pred_dir = (oos_prob > 0.5).astype(int)
            pred_metrics = calculate_predictive_metrics(oos_true, oos_prob)
            calib_metrics = calculate_calibration(oos_true, oos_prob)
        else:
            oos_pred_reg = pd.Series(all_oos_y_pred_reg, index=oos_dates)
            oos_pred_dir = (oos_pred_reg > 0).astype(int)
            corr = np.corrcoef(oos_true, oos_pred_reg)[0, 1] if np.std(oos_pred_reg) > 0 else 0
            pred_metrics = {"correlation": float(corr), "directional_accuracy": float((oos_true > 0) == (oos_pred_reg > 0)).mean()}
            calib_metrics = {"curve": []}

        # Global Trading Metrics
        actual_returns = df_trainable.loc[oos_dates, 'future_return']
        strategy_returns = actual_returns * oos_pred_dir
        buy_hold_returns = actual_returns
        
        trade_metrics = calculate_trading_metrics(strategy_returns)
        bh_metrics = calculate_trading_metrics(buy_hold_returns)
        
        # Baselines
        baselines = {
            "BUY&HOLD": bh_metrics,
            "ASHEN": trade_metrics,
            "MOMENTUM": calculate_trading_metrics(actual_returns * (df_trainable.loc[oos_dates, 'mom_20'] > 0)),
            "SMA20": calculate_trading_metrics(actual_returns * (df_trainable.loc[oos_dates, 'sma_20'] > 1.0))
        }
        
        # Equity Curve
        cum_strategy = (1 + strategy_returns).cumprod()
        cum_bh = (1 + buy_hold_returns).cumprod()
        
        equity_curve = []
        # Sample to max 200 points for frontend rendering speed
        sample_step = max(1, len(oos_dates) // 200)
        
        for i in range(0, len(oos_dates), sample_step):
            idx = oos_dates[i]
            equity_curve.append({
                "date": idx.strftime("%Y-%m-%d"),
                "ASHEN": float(cum_strategy.loc[idx]),
                "BUY_HOLD": float(cum_bh.loc[idx])
            })
            
        # Drawdown Curve
        rolling_max = cum_strategy.cummax()
        drawdown = (cum_strategy - rolling_max) / rolling_max
        drawdown_curve = []
        for i in range(0, len(oos_dates), sample_step):
            idx = oos_dates[i]
            drawdown_curve.append({
                "date": idx.strftime("%Y-%m-%d"),
                "drawdown": float(drawdown.loc[idx])
            })
            
        # Verdict
        verdict = calculate_verdict(
            trade_metrics.get("sharpe_ratio", 0),
            trade_metrics.get("cumulative_return", 0),
            bh_metrics.get("cumulative_return", 0)
        )
        
        # Feature Importance
        feat_imp_result = []
        if len(feature_importances) > 0:
            avg_imp = np.mean(feature_importances, axis=0)
            for i, f in enumerate(features):
                feat_imp_result.append({"feature": f, "importance": float(avg_imp[i])})
            feat_imp_result = sorted(feat_imp_result, key=lambda x: x["importance"], reverse=True)
            
        return {
            "metadata": {
                "symbol": symbol,
                "model": model_name,
                "horizon": horizon,
                "n_folds": n_splits,
                "total_oos_days": len(oos_dates)
            },
            "validation": {
                "purge_window": purge_window,
                "embargo_window": embargo_window,
                "method": "Purged Walk-Forward Cross-Validation"
            },
            "folds": fold_results,
            "predictive_performance": pred_metrics,
            "calibration": calib_metrics,
            "trading_performance": trade_metrics,
            "benchmarks": baselines,
            "equity_curve": equity_curve,
            "drawdown_curve": drawdown_curve,
            "feature_importance": feat_imp_result,
            "verdict": {"status": verdict}
        }
        
    except Exception as e:
        logger.error(f"Validation Job Failed: {traceback.format_exc()}")
        raise Exception(f"Validation Error: {str(e)}")
