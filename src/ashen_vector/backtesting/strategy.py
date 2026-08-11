"""
Trading strategy for translating model predictions into target positions.
"""

import pandas as pd

class SignalStrategy:
    """Strategy that consumes OOS predictions to generate positions."""
    
    def __init__(
        self,
        min_long_probability: float = 0.52,
        min_expected_return: float = 0.001,
        allow_shorts: bool = False
    ):
        self.min_long_probability = min_long_probability
        self.min_expected_return = min_expected_return
        self.allow_shorts = allow_shorts
        
    def generate_signals(self, predictions: pd.DataFrame) -> pd.Series:
        """
        Converts predictions DataFrame into a Series of target positions.
        Returns:
            pd.Series of floats: 1.0 (Long), 0.0 (Flat), -1.0 (Short - if allowed).
        """
        signals = pd.Series(0.0, index=predictions.index, name="target_position")
        
        # Long conditions
        long_cond = (
            (predictions["probability_up"] > self.min_long_probability) & 
            (predictions["expected_return"] > self.min_expected_return)
        )
        
        signals.loc[long_cond] = 1.0
        
        if self.allow_shorts:
            # Short conditions (just an example, not actively used if allow_shorts=False)
            short_cond = (
                (predictions["probability_down"] > self.min_long_probability) & 
                (predictions["expected_return"] < -self.min_expected_return)
            )
            signals.loc[short_cond] = -1.0
            
        return signals
