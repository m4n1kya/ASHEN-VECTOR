"""
Signal generation engine.
Maps quantitative metrics to actionable, but non-guaranteed model signals.
"""
from typing import Dict, Any, Tuple

class SignalEngine:
    """Generates quantitative signals from predictions and confidence."""
    
    @staticmethod
    def generate_signal(
        direction: str,
        expected_return: float,
        confidence_level: str,
        probability_up: float
    ) -> Dict[str, str]:
        """
        Generate a strictly quantitative model signal.
        This does NOT pretend to be a trading recommendation.
        """
        if confidence_level == "LOW":
            return {
                "label": "NEUTRAL",
                "type": "QUANTITATIVE_MODEL_SIGNAL"
            }
            
        if direction == "UP":
            if confidence_level == "HIGH" and expected_return > 0.02 and probability_up > 0.65:
                label = "STRONG_BULLISH"
            else:
                label = "BULLISH"
        else:
            if confidence_level == "HIGH" and expected_return < -0.02 and probability_up < 0.35:
                label = "STRONG_BEARISH"
            else:
                label = "BEARISH"
                
        return {
            "label": label,
            "type": "QUANTITATIVE_MODEL_SIGNAL"
        }
