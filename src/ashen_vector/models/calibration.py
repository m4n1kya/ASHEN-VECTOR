"""
Probability Calibration for classification models.

Calibrates raw model probabilities to reflect true likelihoods using
Platt Scaling (Logistic Regression) or Isotonic Regression.
"""

import numpy as np
import pandas as pd
from typing import Union
from sklearn.linear_model import LogisticRegression
from sklearn.isotonic import IsotonicRegression


class ProbabilityCalibrator:
    """
    Calibrates raw model probabilities.
    Must be fit on an out-of-sample validation set, not the training set.
    """
    
    def __init__(self, method: str = "isotonic"):
        """
        Args:
            method: "isotonic" or "platt" (sigmoid).
        """
        if method not in ["isotonic", "platt"]:
            raise ValueError("Method must be 'isotonic' or 'platt'")
            
        self.method = method
        self.calibrator = None
        self.is_fitted = False
        
    def fit(self, y_prob_raw: np.ndarray, y_true: np.ndarray) -> None:
        """
        Fit the calibrator.
        
        Args:
            y_prob_raw: Raw probabilities from the model (e.g. out-of-fold predictions).
            y_true: True binary labels (0 or 1).
        """
        # Ensure 1D array
        if isinstance(y_prob_raw, pd.Series):
            y_prob_raw = y_prob_raw.values
        if isinstance(y_true, pd.Series):
            y_true = y_true.values
            
        if self.method == "isotonic":
            self.calibrator = IsotonicRegression(out_of_bounds="clip")
            self.calibrator.fit(y_prob_raw, y_true)
        else:
            self.calibrator = LogisticRegression()
            # LogisticRegression expects 2D feature array
            self.calibrator.fit(y_prob_raw.reshape(-1, 1), y_true)
            
        self.is_fitted = True
        
    def predict_proba(self, y_prob_raw: Union[np.ndarray, pd.Series]) -> np.ndarray:
        """
        Calibrate raw probabilities.
        """
        if not self.is_fitted:
            raise RuntimeError("Calibrator is not fitted.")
            
        is_series = isinstance(y_prob_raw, pd.Series)
        index = y_prob_raw.index if is_series else None
        
        if is_series:
            y_prob_raw = y_prob_raw.values
            
        if self.method == "isotonic":
            calibrated = self.calibrator.predict(y_prob_raw)
        else:
            calibrated = self.calibrator.predict_proba(y_prob_raw.reshape(-1, 1))[:, 1]
            
        if is_series:
            return pd.Series(calibrated, index=index)
        return calibrated
