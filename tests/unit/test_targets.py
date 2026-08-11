"""Unit tests for target generation."""

import pandas as pd
import numpy as np

from ashen_vector.features.targets import future_return, future_direction

def test_future_return():
    close = pd.Series([100.0, 105.0, 110.25, 99.225, 100.0])
    
    # 1-day future return
    target_1d = future_return(close, periods=1)
    np.testing.assert_allclose(target_1d.iloc[0], 0.05)  # 105 / 100 - 1
    np.testing.assert_allclose(target_1d.iloc[1], 0.05)  # 110.25 / 105 - 1
    np.testing.assert_allclose(target_1d.iloc[2], -0.10) # 99.225 / 110.25 - 1
    assert pd.isna(target_1d.iloc[-1])
    
    # 2-day future return
    target_2d = future_return(close, periods=2)
    np.testing.assert_allclose(target_2d.iloc[0], 0.1025) # 110.25 / 100 - 1
    assert pd.isna(target_2d.iloc[-1])
    assert pd.isna(target_2d.iloc[-2])

def test_future_direction():
    close = pd.Series([100.0, 105.0, 105.0, 99.225, 100.0])
    
    # 1-day direction
    dir_1d = future_direction(close, periods=1)
    assert dir_1d.iloc[0] == 1.0  # 100 -> 105 (positive)
    assert dir_1d.iloc[1] == 0.0  # 105 -> 105 (zero is not positive)
    assert dir_1d.iloc[2] == 0.0  # 105 -> 99.225 (negative)
    assert dir_1d.iloc[3] == 1.0  # 99.225 -> 100 (positive)
    assert pd.isna(dir_1d.iloc[-1])
