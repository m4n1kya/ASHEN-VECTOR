"""
Confidence Engine for ASHEN-VECTOR.

Explicitly separates the raw model probability (e.g. 73%) from the 
qualitative system confidence (e.g. HIGH).
"""

from typing import Dict, Any, Tuple


class ConfidenceEngine:
    """
    Derives qualitative confidence from model outputs and system metrics.
    """
    
    @staticmethod
    def calculate_confidence(
        probability: float,
        model_accuracy: float,
        data_quality_score: float = 1.0,
        model_agreement: float = 1.0
    ) -> Tuple[str, int]:
        """
        Calculate confidence level and score (0-100).
        
        Args:
            probability: The calibrated probability from the model (0.0 to 1.0).
                         (If regression, this could be a normalized strength signal).
            model_accuracy: The historical out-of-sample accuracy of the model.
            data_quality_score: 0.0 to 1.0 (e.g., penalties for missing volume).
            model_agreement: 0.0 to 1.0 (e.g., if LightGBM and Random Forest agree).
            
        Returns:
            Tuple of (level string, score 0-100).
        """
        # Distance from 0.5 (neutral)
        signal_strength = abs(probability - 0.5) * 2.0  # 0.0 to 1.0
        
        # Penalize models with poor historical accuracy
        # If accuracy is < 0.5, we have no confidence.
        historical_reliability = max(0.0, (model_accuracy - 0.5) * 2.0)
        
        # Base score formula (can be made much more complex later)
        # Weights: 40% signal strength, 40% historical reliability, 10% data quality, 10% agreement
        raw_score = (
            (signal_strength * 40) +
            (historical_reliability * 40) +
            (data_quality_score * 10) +
            (model_agreement * 10)
        )
        
        score = int(min(100, max(0, raw_score)))
        
        if score >= 70:
            level = "HIGH"
        elif score >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"
            
        return level, score
