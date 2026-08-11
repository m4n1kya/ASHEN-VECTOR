"""
Base classes for ASHEN-VECTOR machine learning models.
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any, Tuple


class AshenModel(ABC):
    """Abstract base class for all predictive models."""
    
    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Train the model."""
        pass
        
    @abstractmethod
    def predict(self, X: pd.DataFrame) -> pd.Series:
        """Predict the target variable (probability for classification, magnitude for regression)."""
        pass
        
    @abstractmethod
    def save(self, path: str) -> None:
        """Save model to disk."""
        pass
        
    @classmethod
    @abstractmethod
    def load(cls, path: str) -> 'AshenModel':
        """Load model from disk."""
        pass
        
    def validate_features(self, columns: list[str], feature_whitelist: list[str] = None):
        """Ensure no leakage targets are in the feature set."""
        forbidden = ['future_return', 'future_direction', 'target', 'label', 'forward_return']
        for col in columns:
            if any(f in col for f in forbidden):
                raise ValueError(f"FATAL LEAKAGE: Forbidden column '{col}' detected in features.")
        if feature_whitelist:
            for col in columns:
                if col not in feature_whitelist:
                    raise ValueError(f"FATAL LEAKAGE: Column '{col}' is not in the explicit feature whitelist.")
                    
    def get_feature_importance(self) -> Dict[str, float]:
        """Return feature importance if supported."""
        return {}
