"""
Random Forest model implementation for ASHEN-VECTOR.
Supports both Classification and Regression.
"""

import os
import joblib
import pandas as pd
from typing import Dict, Any, Optional
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from ashen_vector.models.base import AshenModel

class RandomForestModel(AshenModel):
    """Random Forest wrapper for ASHEN-VECTOR."""
    
    def __init__(self, objective: str = "binary", feature_whitelist: list[str] = None, **kwargs):
        """
        Args:
            objective: "binary" for classification, "regression" for continuous target.
            feature_whitelist: Explicit list of allowed features.
            kwargs: RandomForest hyperparameters.
        """
        self.objective = objective
        self.feature_whitelist = feature_whitelist
        self.params = {
            "n_estimators": 100,
            "max_depth": 10,
            "min_samples_split": 5,
            "random_state": 42,
            "n_jobs": -1
        }
        self.params.update(kwargs)
        
        if self.objective == "binary":
            self.model = RandomForestClassifier(**self.params)
        else:
            self.model = RandomForestRegressor(**self.params)
            
        self.feature_names = []
        self.is_trained = False
        
    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.validate_features(list(X.columns), self.feature_whitelist)
        self.feature_names = list(X.columns)
        
        # Scikit-learn doesn't handle NaNs by default in RF
        # Basic fillna for MVP; real system should have robust imputation in FeaturePipeline
        X_clean = X.fillna(0)
        
        self.model.fit(X_clean, y)
        self.is_trained = True
        
    def predict(self, X: pd.DataFrame) -> pd.Series:
        if not self.is_trained:
            raise RuntimeError("Model is not trained.")
            
        self.validate_features(list(X.columns), self.feature_whitelist)
        X = X[self.feature_names].fillna(0)
        
        if self.objective == "binary":
            preds = self.model.predict_proba(X)[:, 1]
        else:
            preds = self.model.predict(X)
            
        return pd.Series(preds, index=X.index)
        
    def save(self, path: str) -> None:
        if not self.is_trained:
            raise RuntimeError("Cannot save an untrained model.")
            
        os.makedirs(os.path.dirname(path), exist_ok=True)
        state = {
            "model_type": "RandomForestModel",
            "objective": self.objective,
            "params": self.params,
            "feature_names": self.feature_names,
            "feature_whitelist": self.feature_whitelist,
            "sklearn_model": self.model
        }
        joblib.dump(state, path)
        
    @classmethod
    def load(cls, path: str) -> 'RandomForestModel':
        state = joblib.load(path)
        
        instance = cls(objective=state["objective"], feature_whitelist=state.get("feature_whitelist"))
        instance.params = state["params"]
        instance.feature_names = state["feature_names"]
        instance.model = state["sklearn_model"]
        instance.is_trained = True
        
        return instance
        
    def get_feature_importance(self) -> Dict[str, float]:
        if not self.is_trained:
            return {}
        importance = self.model.feature_importances_
        return dict(zip(self.feature_names, importance))
