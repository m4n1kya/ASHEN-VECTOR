"""Unit tests for the feature pipeline and critical leakage checks."""

import pandas as pd
import numpy as np
import pytest
from unittest.mock import MagicMock

from ashen_vector.features.pipeline import FeaturePipeline

@pytest.fixture
def mock_provider():
    provider = MagicMock()
    # Generate 100 days of mock data
    dates = pd.date_range("2020-01-01", periods=100)
    df = pd.DataFrame({
        "$open": np.random.uniform(90, 110, 100),
        "$high": np.random.uniform(110, 120, 100),
        "$low": np.random.uniform(80, 90, 100),
        "$close": np.random.uniform(95, 115, 100),
        "$volume": np.random.uniform(1000, 5000, 100)
    }, index=dates)
    
    def get_history(symbol, start_date, end_date, fields=None):
        return df.copy()
        
    provider.get_history = get_history
    provider.instrument_exists.return_value = True
    provider.is_initialized.return_value = True
    return provider

def test_feature_leakage_audit(mock_provider):
    """
    CRITICAL TEST: Modify future values and verify past features DO NOT change.
    """
    pipeline = FeaturePipeline(mock_provider)
    
    # Baseline features
    features_base = pipeline.build_features("TEST", "2020-03-01", "2020-04-10")
    
    # Modify data in the provider at t+10
    original_df = mock_provider.get_history("TEST", "1990", "2030")
    modified_df = original_df.copy()
    
    # Change the close price significantly on day 80
    modification_date = modified_df.index[80]
    modified_df.loc[modification_date, "$close"] = 9999.0
    modified_df.loc[modification_date, "$high"] = 9999.0
    modified_df.loc[modification_date, "$low"] = 9999.0
    modified_df.loc[modification_date, "$open"] = 9999.0
    modified_df.loc[modification_date, "$volume"] = 99999999.0
    
    # Update mock to return modified data
    def get_modified_history(symbol, start_date=None, end_date=None, **kwargs):
        return modified_df.copy()
    
    mock_provider.get_history = get_modified_history
    
    # Recompute features
    features_modified = pipeline.build_features("TEST", "2020-03-01", "2020-04-10")
    
    # Ensure the modification date is in our resulting features to test the split
    assert modification_date in features_modified.index
    
    # For every date strictly BEFORE the modification date, features MUST be identical
    before_mod_base = features_base.loc[:modification_date - pd.Timedelta(days=1)]
    before_mod_mod = features_modified.loc[:modification_date - pd.Timedelta(days=1)]
    
    pd.testing.assert_frame_equal(before_mod_base, before_mod_mod)
    
def test_target_separation(mock_provider):
    """Verify that targets are not leaked into the feature matrix."""
    pipeline = FeaturePipeline(mock_provider)
    
    X, y = pipeline.build_training_dataset("TEST", "2020-03-01", "2020-04-10")
    
    # Verify strict disjoint sets
    assert set(X.columns).isdisjoint(set(y.columns)), "Target columns found in feature matrix X!"
