import pytest
import pandas as pd
from ashen_vector.models.base import AshenModel
from ashen_vector.models.lightgbm_model import LightGBMModel

def test_model_rejects_leakage_columns():
    """Ensure models reject forbidden target columns at runtime."""
    model = LightGBMModel()
    
    # Try to predict with a forbidden column
    X_bad = pd.DataFrame({"future_return_5d": [0.01, -0.02]})
    
    with pytest.raises(ValueError, match="FATAL LEAKAGE"):
        model.train(X_bad, pd.Series([1, 0]))
        
    X_bad2 = pd.DataFrame({"target": [1, 0]})
    with pytest.raises(ValueError, match="FATAL LEAKAGE"):
        model.train(X_bad2, pd.Series([1, 0]))

def test_model_rejects_non_whitelist_columns():
    """Ensure models reject any column not in explicit whitelist."""
    whitelist = ["feature_a", "feature_b"]
    model = LightGBMModel(feature_whitelist=whitelist)
    
    X_bad = pd.DataFrame({
        "feature_a": [1, 2],
        "feature_b": [3, 4],
        "rogue_feature": [5, 6]
    })
    
    with pytest.raises(ValueError, match="FATAL LEAKAGE: Column 'rogue_feature' is not in the explicit feature whitelist"):
        model.train(X_bad, pd.Series([1, 0]))
        
def test_predict_rejects_non_whitelist():
    """Ensure predict also enforces the whitelist."""
    whitelist = ["feature_a", "feature_b"]
    model = LightGBMModel(feature_whitelist=whitelist)
    
    X_train = pd.DataFrame({"feature_a": [1, 2], "feature_b": [3, 4]})
    model.train(X_train, pd.Series([1, 0]))
    
    X_pred = pd.DataFrame({"feature_a": [1], "feature_b": [3], "leak": [0]})
    
    with pytest.raises(ValueError, match="FATAL LEAKAGE"):
        model.predict(X_pred)
