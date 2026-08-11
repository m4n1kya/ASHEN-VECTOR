"""
Validation logic for ASHEN-VECTOR.

Implements Purged Walk-Forward Cross Validation to eliminate look-ahead bias
and temporal leakage in time-series machine learning models.
"""

import numpy as np
import pandas as pd
from typing import Generator, Tuple, Optional


class PurgedWalkForwardCV:
    """
    Purged Walk-Forward Cross Validation.
    
    This validator ensures that train and test sets do not leak information, 
    which is absolutely critical for time-series models with overlapping targets.
    
    Why these parameters exist:
    
    1. TARGET_HORIZON (n): The number of periods ahead the model predicts (e.g., 5 days).
       Because the target at time T depends on data from T to T+5, any observation 
       in the training set within 5 days BEFORE the start of the validation set will
       have a target constructed using data that overlaps with the validation features.
       
    2. PURGE_WINDOW (p): The number of observations removed from the END of the training 
       set to prevent overlapping targets. Usually, p >= n.
       
    3. EMBARGO_WINDOW (e): The number of observations removed from the START of the 
       subsequent training set (if train sets are formed after validation sets, or if 
       doing full K-fold). This prevents the model from peeking at the validation 
       set's outcome through subsequent features (like a moving average incorporating 
       a test-set price shock).
    """
    
    def __init__(
        self,
        n_splits: int = 5,
        target_horizon: int = 5,
        purge_window: int = 5,
        embargo_window: int = 5,
        min_train_size: Optional[int] = None
    ):
        self.n_splits = n_splits
        self.target_horizon = target_horizon
        self.purge_window = purge_window
        self.embargo_window = embargo_window
        self.min_train_size = min_train_size
        
    def split(self, X: pd.DataFrame, y: pd.DataFrame = None) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """
        Generate indices to split data into training and test sets.
        
        Yields:
            train (np.ndarray): The training set indices for that split.
            test (np.ndarray): The testing set indices for that split.
        """
        n_samples = len(X)
        indices = np.arange(n_samples)
        
        # Test size is roughly the remaining data after min_train_size, divided by n_splits
        # Or simple walk forward: split data into n_splits + 1 chunks.
        chunk_size = n_samples // (self.n_splits + 1)
        
        if self.min_train_size is None:
            min_train = chunk_size
        else:
            min_train = self.min_train_size
            
        for i in range(self.n_splits):
            # Test set window
            test_start = n_samples - chunk_size * (self.n_splits - i)
            test_end = test_start + chunk_size
            
            # Train set window (expanding window approach)
            train_start = 0
            
            # The raw train end would normally be test_start
            raw_train_end = test_start
            
            # 1. PURGING: Remove `purge_window` observations BEFORE the test set
            train_end = max(0, raw_train_end - self.purge_window)
            
            # If train_end is less than train_start + min_train, we don't have enough data
            if train_end < min_train:
                continue
                
            train_indices = indices[train_start:train_end]
            test_indices = indices[test_start:test_end]
            
            # Note: Embargo applies if we use observations AFTER the test set in the train set 
            # (e.g., standard K-fold). Since this is an Expanding Walk-Forward, the train set 
            # is always strictly BEFORE the test set. 
            # However, for completeness, if we ever implement Combinatorial Purged CV, 
            # the embargo would drop `embargo_window` observations immediately following the test set.
            
            yield train_indices, test_indices
