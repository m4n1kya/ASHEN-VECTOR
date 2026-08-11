import pytest
import pandas as pd
import numpy as np
from ashen_vector.models.validation import PurgedWalkForwardCV

def test_purged_walk_forward_cv():
    # Create 100 observations
    dates = pd.date_range("2020-01-01", periods=100, freq="D")
    X = pd.DataFrame({"feature1": np.random.randn(100)}, index=dates)
    
    cv = PurgedWalkForwardCV(
        n_splits=3,
        target_horizon=5,
        purge_window=5,
        embargo_window=5,
        min_train_size=10
    )
    
    splits = list(cv.split(X))
    
    # 3 splits
    assert len(splits) == 3
    
    chunk_size = 100 // 4  # 25
    
    for i, (train_idx, test_idx) in enumerate(splits):
        # The test set shouldn't overlap with train set
        assert len(set(train_idx).intersection(set(test_idx))) == 0
        
        # Test sets should be chunk_size
        assert len(test_idx) == chunk_size
        
        # In Expanding Walk-Forward, train is strictly before test
        assert max(train_idx) < min(test_idx)
        
        # Verify the purge window (gap between train and test)
        gap = min(test_idx) - max(train_idx)
        assert gap == cv.purge_window + 1  # If test starts at 75, and max train is 69, gap is 6 (indexes 70, 71, 72, 73, 74 dropped)
        
        if i == 0:
            # First split: test is 25-49, train is 0-19
            assert min(test_idx) == 25
            assert max(test_idx) == 49
            assert max(train_idx) == 19
        elif i == 1:
            # Second split: test is 50-74, train is 0-44
            assert min(test_idx) == 50
            assert max(test_idx) == 74
            assert max(train_idx) == 44
