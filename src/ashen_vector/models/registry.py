"""
Model registry for saving, loading, and managing trained ASHEN-VECTOR models and their metadata.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from ashen_vector.models.base import AshenModel
from ashen_vector.models.lightgbm_model import LightGBMModel
from ashen_vector.models.random_forest import RandomForestModel

# Map string types to classes
MODEL_TYPES = {
    "lightgbm": LightGBMModel,
    "random_forest": RandomForestModel
}

class ModelRegistry:
    """Manages model artifacts and metadata."""
    
    def __init__(self, base_dir: str = "models"):
        self.base_dir = base_dir
        self.artifacts_dir = os.path.join(base_dir, "artifacts")
        self.metadata_dir = os.path.join(base_dir, "metadata")
        self.features_dir = os.path.join(base_dir, "feature_analysis")
        
        os.makedirs(self.artifacts_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
        os.makedirs(self.features_dir, exist_ok=True)
        
    def _get_git_commit(self) -> str:
        """Attempt to get the current git commit for reproducibility."""
        try:
            import subprocess
            return subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL).decode('ascii').strip()
        except Exception:
            return "unknown"
            
    def save_model(
        self, 
        model_id: str,
        model: AshenModel, 
        model_type: str,
        target: str,
        horizon: int,
        trained_from: str,
        trained_until: str,
        metrics: Dict[str, Any],
        validation_method: str = "purged_walk_forward",
        calibration: str = "none",
        feature_version: str = "v001",
        model_version: str = "v001",
        feature_analysis: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save a trained model and its metadata.
        Returns the path to the saved model artifact.
        """
        artifact_path = os.path.join(self.artifacts_dir, f"{model_id}.joblib")
        metadata_path = os.path.join(self.metadata_dir, f"{model_id}.json")
        
        # Save model weights
        model.save(artifact_path)
        
        # Save feature analysis if provided
        if feature_analysis:
            analysis_path = os.path.join(self.features_dir, f"{model_id}.json")
            with open(analysis_path, 'w') as f:
                json.dump(feature_analysis, f, indent=2)
        
        # Save metadata
        metadata = {
            "model_id": model_id,
            "model_version": model_version,
            "feature_version": feature_version,
            "model_type": model_type,
            "target": target,
            "horizon": horizon,
            "trained_from": trained_from,
            "trained_until": trained_until,
            "validation": validation_method,
            "calibration": calibration,
            "metrics": metrics,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "git_commit": self._get_git_commit(),
            "artifact_path": artifact_path
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        return artifact_path
        
    def load_model(self, model_id: str) -> AshenModel:
        """Load a model by ID."""
        metadata_path = os.path.join(self.metadata_dir, f"{model_id}.json")
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Model metadata not found: {metadata_path}")
            
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            
        model_type = metadata["model_type"]
        if model_type not in MODEL_TYPES:
            raise ValueError(f"Unknown model type: {model_type}")
            
        model_cls = MODEL_TYPES[model_type]
        artifact_path = metadata["artifact_path"]
        
        return model_cls.load(artifact_path)
        
    def get_metadata(self, model_id: str) -> Dict[str, Any]:
        """Get model metadata."""
        metadata_path = os.path.join(self.metadata_dir, f"{model_id}.json")
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Model metadata not found: {metadata_path}")
            
        with open(metadata_path, 'r') as f:
            return json.load(f)
            
    def list_models(self) -> Dict[str, Dict[str, Any]]:
        """List all available models and their metadata."""
        models = {}
        for filename in os.listdir(self.metadata_dir):
            if filename.endswith(".json"):
                model_id = filename[:-5]
                try:
                    models[model_id] = self.get_metadata(model_id)
                except Exception:
                    pass
        return models
