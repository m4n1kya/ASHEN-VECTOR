"""
Model metadata API schemas.
"""
from pydantic import BaseModel
from typing import Dict, Any, List

class ModelMetadata(BaseModel):
    model_id: str
    type: str
    version: str
    target: str
    horizon: int
    validation: str
    calibration: str
    status: str
    metrics: Dict[str, Any]

class StockModelsResponse(BaseModel):
    symbol: str
    models: List[ModelMetadata]
