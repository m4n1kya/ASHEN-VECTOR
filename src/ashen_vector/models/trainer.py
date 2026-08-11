"""
Model training orchestrator.

Handles data fetching, validation splitting, model training, metric computation,
performance gating against baselines, and model registry persistence.
"""

import pandas as pd
from typing import Dict, Any, Optional, Tuple

from ashen_vector.features.pipeline import FeaturePipeline
from ashen_vector.models.base import AshenModel
from ashen_vector.models.registry import ModelRegistry
from ashen_vector.models.validation import PurgedWalkForwardCV
from ashen_vector.models.metrics import classification_metrics, regression_metrics
from ashen_vector.models.baselines import PredictiveBaselines


class ModelTrainer:
    """Orchestrates the entire ML pipeline from data to saved model."""
    
    def __init__(self, feature_pipeline: FeaturePipeline, registry: ModelRegistry):
        self.pipeline = feature_pipeline
        self.registry = registry
        
    def _evaluate_model(self, model: AshenModel, X_test: pd.DataFrame, y_test: pd.Series, objective: str) -> Dict[str, float]:
        """Compute metrics for model on test set."""
        preds = model.predict(X_test)
        if objective == "binary":
            return classification_metrics(y_test, preds)
        else:
            return regression_metrics(y_test, preds)
            
    def train_and_evaluate(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        model_cls: type,
        model_kwargs: Dict[str, Any],
        objective: str,
        target_col: str,
        horizon: int
    ) -> Tuple[AshenModel, Dict[str, float], Dict[str, float]]:
        """
        Train a model using Purged Walk-Forward CV and evaluate against baselines.
        Returns (trained_model, model_metrics, baseline_metrics).
        """
        # 1. Get complete dataset (features + target)
        X, y = self.pipeline.build_training_dataset(symbol, start_date, end_date, target_col)
        
        # We need a validation strategy. For now, to get a single deployable model, 
        # we can train on expanding windows and take the metrics of the final fold,
        # or we could aggregate metrics across folds.
        # Then, we retrain the final model on the ENTIRE dataset to maximize information.
        
        cv = PurgedWalkForwardCV(
            n_splits=3,
            target_horizon=horizon,
            purge_window=horizon,
            embargo_window=horizon
        )
        
        # Aggregate metrics across folds
        fold_metrics = []
        baseline_metrics = []
        fold_importances = []
        
        feature_whitelist = self.pipeline.get_feature_names()
        
        for train_idx, test_idx in cv.split(X):
            X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
            X_test, y_test = X.iloc[test_idx], y.iloc[test_idx]
            
            # Train model
            fold_model = model_cls(objective=objective, feature_whitelist=feature_whitelist, **model_kwargs)
            fold_model.train(X_train, y_train)
            
            # Record feature importance for this fold
            fold_importances.append(fold_model.get_feature_importance())
            
            # Eval model
            metrics = self._evaluate_model(fold_model, X_test, y_test, objective)
            fold_metrics.append(metrics)
            
            # Eval baseline (Majority class for CLS, Previous Return for REG)
            if objective == "binary":
                base_preds = PredictiveBaselines.majority_class(y_train, y_test)
                base_mets = classification_metrics(y_test, base_preds)
            else:
                base_preds = PredictiveBaselines.previous_return(X_test)
                base_mets = regression_metrics(y_test, base_preds)
                
            baseline_metrics.append(base_mets)
            
        # Average metrics
        avg_metrics = pd.DataFrame(fold_metrics).mean().to_dict()
        avg_base_metrics = pd.DataFrame(baseline_metrics).mean().to_dict()
        
        # 2. Retrain final model on all data
        final_model = model_cls(objective=objective, feature_whitelist=feature_whitelist, **model_kwargs)
        final_model.train(X, y)
        global_importance = final_model.get_feature_importance()
        
        # Feature Stability Analysis
        df_imp = pd.DataFrame(fold_importances)
        stability = (df_imp.mean() / (df_imp.std() + 1e-9)).to_dict()
        
        # Top Features
        top_features = pd.Series(global_importance).sort_values(ascending=False).head(20).to_dict()
        
        feature_analysis = {
            "global_importance": global_importance,
            "fold_importance": fold_importances,
            "stability": stability,
            "top_features": top_features
        }
        
        return final_model, avg_metrics, avg_base_metrics, feature_analysis
        
    def run_training_job(
        self,
        job_id: str,
        symbol: str,
        start_date: str,
        end_date: str,
        model_cls: type,
        model_kwargs: Dict[str, Any],
        objective: str,
        target_col: str,
        horizon: int
    ) -> Dict[str, Any]:
        """
        Runs the full training job, applies the performance gate, and saves the model.
        Returns job status dictionary.
        """
        try:
            model, metrics, base_metrics, feature_analysis = self.train_and_evaluate(
                symbol, start_date, end_date, model_cls, model_kwargs, objective, target_col, horizon
            )
            
            # PERFORMANCE GATE
            passed = False
            if objective == "binary":
                # Must beat majority class accuracy by at least 1%
                passed = metrics.get("accuracy", 0) > (base_metrics.get("accuracy", 0) + 0.01)
            else:
                # Must beat previous return IC or RMSE
                passed = metrics.get("rmse", 999) < base_metrics.get("rmse", 999)
                
            if passed:
                model_id = f"ashen_{symbol}_{objective}_{horizon}d"
                
                # Combine metrics with baseline for saving
                all_metrics = {
                    "model": metrics,
                    "baseline": base_metrics
                }
                
                path = self.registry.save_model(
                    model_id=model_id,
                    model=model,
                    model_type=model_cls.__name__,
                    target=target_col,
                    horizon=horizon,
                    trained_from=start_date,
                    trained_until=end_date,
                    metrics=all_metrics,
                    validation_method="purged_walk_forward",
                    feature_analysis=feature_analysis
                )
                
                return {
                    "job_id": job_id,
                    "status": "completed",
                    "result": "passed",
                    "model_id": model_id,
                    "metrics": metrics
                }
            else:
                return {
                    "job_id": job_id,
                    "status": "completed",
                    "result": "failed_gate",
                    "reason": "Model did not beat baseline.",
                    "metrics": metrics,
                    "baseline": base_metrics
                }
                
        except Exception as e:
            import traceback
            return {
                "job_id": job_id,
                "status": "failed",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
