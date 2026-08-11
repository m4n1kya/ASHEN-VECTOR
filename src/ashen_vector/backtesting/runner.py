"""
Backtest execution runner.
Iterates over time, trains models on expanding windows, and generates Out-of-Sample predictions.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

from ashen_vector.features.pipeline import FeaturePipeline
from ashen_vector.models.validation import PurgedWalkForwardCV
from ashen_vector.models.lightgbm_model import LightGBMModel

class WalkForwardRunner:
    """Generates true out-of-sample predictions using Purged Walk-Forward CV."""
    
    def __init__(self, pipeline: FeaturePipeline):
        self.pipeline = pipeline
        
    def generate_oos_predictions(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str, 
        horizon: int,
        n_splits: int = 5
    ) -> pd.DataFrame:
        """
        Runs the full walk-forward process and returns only Out-Of-Sample predictions.
        """
        # 1. Fetch features and BOTH targets (classification and regression)
        # We need to build a custom dataset combining both targets to train both models
        
        # Build features
        X = self.pipeline.build_features(symbol, start_date, end_date)
        feature_whitelist = self.pipeline.get_feature_names()
        
        # Use the pipeline's built-in target fetch to ensure identical padding logic
        X_cls, y_cls_series = self.pipeline.build_training_dataset(symbol, start_date, end_date, f"direction_{horizon}d")
        X_reg, y_reg_series = self.pipeline.build_training_dataset(symbol, start_date, end_date, f"future_return_{horizon}d")
        
        # Align them perfectly
        X = X_cls
        y_cls_aligned = y_cls_series.to_frame(name="direction")
        y_reg_aligned = y_reg_series.to_frame(name="return")
        
        feature_whitelist = self.pipeline.get_feature_names()
        
        # We need the close prices for the portfolio simulator (entry/exit execution)
        close_p = self.pipeline.provider.get_history(symbol, start_date=start_date, end_date=end_date)["$close"]
        
        cv = PurgedWalkForwardCV(
            n_splits=n_splits,
            target_horizon=horizon,
            purge_window=horizon,
            embargo_window=horizon
        )
        
        oos_predictions = []
        
        for train_idx, test_idx in cv.split(X):
            X_train = X.iloc[train_idx]
            X_test = X.iloc[test_idx]
            
            y_train_cls = y_cls_aligned.iloc[train_idx]["direction"]
            y_train_reg = y_reg_aligned.iloc[train_idx]["return"]
            
            # Train Classifier
            cls_model = LightGBMModel(objective="binary", feature_whitelist=feature_whitelist)
            cls_model.train(X_train, y_train_cls)
            
            # Train Regressor
            reg_model = LightGBMModel(objective="regression", feature_whitelist=feature_whitelist)
            reg_model.train(X_train, y_train_reg)
            
            # Predict OOS
            preds_cls = cls_model.predict(X_test)
            preds_reg = reg_model.predict(X_test)
            
            fold_df = pd.DataFrame({
                "probability_up": preds_cls,
                "probability_down": 1.0 - preds_cls,
                "expected_return": preds_reg,
                "actual_return": y_reg_aligned.iloc[test_idx]["return"],
                "actual_direction": y_cls_aligned.iloc[test_idx]["direction"],
                "close": close_p.loc[X_test.index]
            }, index=X_test.index)
            
            oos_predictions.append(fold_df)
            
        if not oos_predictions:
            return pd.DataFrame()
            
        final_oos = pd.concat(oos_predictions).sort_index()
        # Remove any potential overlapping duplicates from boundaries
        final_oos = final_oos[~final_oos.index.duplicated(keep='first')]
        
        return final_oos

def run_full_backtest(
    symbol: str, 
    start_date: str, 
    end_date: str, 
    horizon: int,
    initial_capital: float,
    strategy_name: str,
    commission_bps: int,
    slippage_bps: int,
    pipeline: FeaturePipeline
) -> dict:
    """Orchestrates the entire backtest, generating the full report."""
    from ashen_vector.backtesting.strategy import SignalStrategy
    from ashen_vector.backtesting.engine import BacktestEngine
    from ashen_vector.backtesting.costs import TransactionCosts
    from ashen_vector.backtesting.benchmarks import Benchmarks
    from ashen_vector.backtesting.metrics import (
        calculate_predictive_metrics, 
        calculate_trading_metrics, 
        calculate_risk_metrics,
        generate_model_verdict
    )
    
    runner = WalkForwardRunner(pipeline)
    
    # 1. Get OOS Predictions
    oos_preds = runner.generate_oos_predictions(symbol, start_date, end_date, horizon)
    if oos_preds.empty:
        raise ValueError("No out-of-sample predictions generated.")
        
    # 2. Generate Signals
    if strategy_name == "ashen_vector":
        strategy = SignalStrategy()
        signals = strategy.generate_signals(oos_preds)
    else:
        signals = pd.Series(0.0, index=oos_preds.index)
        
    # 3. Setup Costs
    costs = TransactionCosts(
        commission_rate=commission_bps / 10000.0,
        slippage_rate=slippage_bps / 10000.0
    )
    
    # 4. Run Model Backtest
    engine = BacktestEngine(initial_capital, costs)
    prices = oos_preds["close"]
    model_equity = engine.run(symbol, prices, signals)
    
    # 5. Run Benchmark Backtests
    buy_hold_sigs = Benchmarks.buy_and_hold(prices)
    buy_hold_equity = BacktestEngine(initial_capital, costs).run(symbol, prices, buy_hold_sigs)
    
    mom_sigs = Benchmarks.momentum_strategy(prices)
    mom_equity = BacktestEngine(initial_capital, costs).run(symbol, prices, mom_sigs)
    
    sma_sigs = Benchmarks.sma_crossover(prices)
    sma_equity = BacktestEngine(initial_capital, costs).run(symbol, prices, sma_sigs)
    
    # 6. Calculate Metrics
    predictive = calculate_predictive_metrics(oos_preds)
    
    model_metrics = {
        "trading_performance": calculate_trading_metrics(model_equity),
        "risk_metrics": calculate_risk_metrics(model_equity)
    }
    
    bh_metrics = {
        "trading_performance": calculate_trading_metrics(buy_hold_equity),
        "risk_metrics": calculate_risk_metrics(buy_hold_equity)
    }
    mom_metrics = {
        "trading_performance": calculate_trading_metrics(mom_equity),
        "risk_metrics": calculate_risk_metrics(mom_equity)
    }
    sma_metrics = {
        "trading_performance": calculate_trading_metrics(sma_equity),
        "risk_metrics": calculate_risk_metrics(sma_equity)
    }
    
    # 7. Verdict
    verdict = generate_model_verdict(model_metrics, bh_metrics)
    
    # 8. Report
    return {
        "predictive_performance": predictive,
        "trading_performance": model_metrics["trading_performance"],
        "risk_metrics": model_metrics["risk_metrics"],
        "benchmark_comparison": {
            "buy_and_hold": bh_metrics,
            "momentum": mom_metrics,
            "sma20": sma_metrics,
            "verdict": verdict
        }
    }
