"""
Endpoints for running inference via trained models.
"""
from fastapi import APIRouter, HTTPException

from ashen_vector.api.schemas.predictions import PredictionRequest, PredictionResponse
from ashen_vector.data.qlib_provider import get_provider
from ashen_vector.features.pipeline import FeaturePipeline
from ashen_vector.models.registry import ModelRegistry
from ashen_vector.predictions.engine import PredictionEngine

router = APIRouter(prefix="/predictions", tags=["predictions"])

def get_prediction_engine() -> PredictionEngine:
    provider = get_provider()
    pipeline = FeaturePipeline(provider)
    registry = ModelRegistry()
    return PredictionEngine(registry, pipeline)

@router.post("/predict", response_model=PredictionResponse, summary="Run inference for a symbol")
async def run_prediction(request: PredictionRequest):
    try:
        engine = get_prediction_engine()
        
        result = engine.predict(
            symbol=request.symbol,
            horizon=request.horizon,
            classifier_id=request.classifier_id,
            regressor_id=request.regressor_id,
            date=request.date
        )
        
        return PredictionResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
