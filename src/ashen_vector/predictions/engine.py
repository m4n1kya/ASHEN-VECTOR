"""
Inference engine combining classification, regression, and confidence.
"""

from typing import Dict, Any, Optional
import pandas as pd
from ashen_vector.models.registry import ModelRegistry
from ashen_vector.predictions.confidence import ConfidenceEngine
from ashen_vector.features.pipeline import FeaturePipeline
from ashen_vector.predictions.signal import SignalEngine
from ashen_vector.config.settings import get_settings

class PredictionEngine:
    """Unifies ML models to generate complete prediction objects."""
    
    def __init__(self, registry: ModelRegistry, feature_pipeline: FeaturePipeline):
        self.registry = registry
        self.feature_pipeline = feature_pipeline
        self.loaded_models = {}
        
    def _get_model(self, model_id: str):
        """Lazy load and cache models."""
        if model_id not in self.loaded_models:
            self.loaded_models[model_id] = self.registry.load_model(model_id)
        return self.loaded_models[model_id]
        
    def predict(
        self, 
        symbol: str, 
        horizon: int, 
        classifier_id: str, 
        regressor_id: Optional[str] = None,
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a unified prediction for a given symbol.
        """
        # Load metadata first to check availability and gate status
        try:
            cls_meta = self.registry.get_metadata(classifier_id)
            cls_model = self._get_model(classifier_id)
        except Exception:
            import datetime
            dt = date if date else datetime.datetime.now().strftime("%Y-%m-%d")
            return {
                "symbol": symbol,
                "date": dt,
                "status": "MODEL_UNAVAILABLE",
                "prediction": {
                    "status": "MODEL_UNAVAILABLE",
                    "direction": None,
                    "probability_up": None,
                    "probability_down": None,
                    "expected_return": None
                }
            }
            
        reg_meta = None
        if regressor_id:
            try:
                reg_meta = self.registry.get_metadata(regressor_id)
                reg_model = self._get_model(regressor_id)
            except Exception:
                pass
                
        import datetime
        end_date = date if date else datetime.datetime.now().strftime("%Y-%m-%d")
        start_date = (pd.to_datetime(end_date) - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
        
        try:
            features_df = self.feature_pipeline.build_features(symbol, start_date, end_date)
            if features_df.empty:
                raise ValueError(f"No features available for {symbol} at {end_date}")
            latest_features = features_df.iloc[[-1]]
            target_date = latest_features.index[0]
        except Exception as e:
            raise RuntimeError(f"Feature generation failed: {e}")
            
        # VERY IMPORTANT: Hard safety barrier against look-ahead bias
        settings = get_settings()
        forbidden = settings.forbidden_inference_columns
        overlap = set(latest_features.columns).intersection(forbidden)
        assert not overlap, f"FATAL LEAKAGE: Inference vector contains forbidden columns {overlap}"

        # 2. Classification
        prob_up = float(cls_model.predict(latest_features).iloc[0])
        prob_down = 1.0 - prob_up
        direction = "UP" if prob_up > 0.5 else "DOWN"
        
        # 3. Regression
        expected_return = None
        if reg_meta:
            expected_return = float(reg_model.predict(latest_features).iloc[0])
            
        # 4. Confidence
        accuracy = cls_meta.get("metrics", {}).get("model", {}).get("accuracy", 0.5)
        if "metrics" in cls_meta and "accuracy" in cls_meta["metrics"]:
             accuracy = cls_meta["metrics"]["accuracy"]
             
        level, score = ConfidenceEngine.calculate_confidence(
            probability=prob_up,
            model_accuracy=accuracy
        )
        
        # 5. Signal
        signal_data = SignalEngine.generate_signal(
            direction=direction,
            expected_return=expected_return or 0.0,
            confidence_level=level,
            probability_up=prob_up
        )
        
        if hasattr(target_date, "strftime"):
            target_date = target_date.strftime("%Y-%m-%d")
        elif hasattr(target_date, "__len__") and len(target_date) == 2:
            target_date = target_date[1].strftime("%Y-%m-%d")
        else:
            target_date = str(target_date)
            
        payload = {
            "status": "ACTIVE",
            "symbol": symbol,
            "date": target_date,
            "prediction": {
                "direction": direction,
                "probability_up": prob_up,
                "probability_down": prob_down,
                "expected_return": expected_return
            },
            "confidence": {
                "level": level,
                "score": score
            },
            "signal": signal_data,
            "models": {
                "classification": {
                    "id": classifier_id,
                    "type": cls_meta["model_type"],
                    "version": cls_meta["model_version"]
                }
            }
        }
        
        if reg_meta:
            payload["models"]["regression"] = {
                "id": regressor_id,
                "type": reg_meta["model_type"],
                "version": reg_meta["model_version"]
            }
            
        return payload
