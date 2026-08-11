"""
LightGBM model implementation for ASHEN-VECTOR.
Supports both Classification and Regression.
"""

import os
import joblib
import pandas as pd
import lightgbm as lgb
from typing import Dict, Any, Optional
from ashen_vector.models.base import AshenModel

class LightGBMModel(AshenModel):
    """LightGBM wrapper for ASHEN-VECTOR."""
    
    def __init__(self, objective: str = "binary", feature_whitelist: list[str] = None, **kwargs):
        """
        Args:
            objective: "binary" for classification, "regression" for continuous target.
            feature_whitelist: Explicit list of allowed features.
            kwargs: LightGBM hyperparameters.
        """
        self.objective = objective
        self.feature_whitelist = feature_whitelist
        self.params = {
            "objective": objective,
            "metric": "binary_logloss" if objective == "binary" else "rmse",
            "boosting_type": "gbdt",
            "learning_rate": 0.05,
            "num_leaves": 31,
            "max_depth": -1,
            "feature_fraction": 0.8,
            "verbosity": -1,
            "random_state": 42
        }
        self.params.update(kwargs)
        self.model: Optional[lgb.Booster] = None
        self.feature_names = []
        
    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.validate_features(list(X.columns), self.feature_whitelist)
        self.feature_names = list(X.columns)
        
        train_data = lgb.Dataset(X, label=y)
        
        # In a real setup, we might pass early stopping validation sets here
        # But for the base train method, we just fit
        self.model = lgb.train(
            self.params,
            train_data,
            num_boost_round=100
        )
        
    def predict(self, X: pd.DataFrame) -> pd.Series:
        if self.model is None:
            raise RuntimeError("Model is not trained.")
            
        # Ensure column order matches and whitelist is respected
        self.validate_features(list(X.columns), self.feature_whitelist)
        X = X[self.feature_names]
        
        preds = self.model.predict(X)
        return pd.Series(preds, index=X.index)
        
    def save(self, path: str) -> None:
        if self.model is None:
            raise RuntimeError("Cannot save an untrained model.")
            
        os.makedirs(os.path.dirname(path), exist_ok=True)
        state = {
            "model_type": "LightGBMModel",
            "objective": self.objective,
            "params": self.params,
            "feature_names": self.feature_names,
            "feature_whitelist": self.feature_whitelist,
            # We save the model string representation or dump it
            "booster": self.model.model_to_string()
        }
        joblib.dump(state, path)
        
    @classmethod
    def load(cls, path: str) -> 'LightGBMModel':
        state = joblib.load(path)
        
        instance = cls(objective=state["objective"], feature_whitelist=state.get("feature_whitelist"))
        instance.params = state["params"]
        instance.feature_names = state["feature_names"]
        
        instance.model = lgb.Booster(model_str=state["booster"])
        return instance
        
    def get_feature_importance(self) -> Dict[str, float]:
        if self.model is None:
            return {}
        importance = self.model.feature_importance(importance_type="gain")
        return dict(zip(self.feature_names, importance))
