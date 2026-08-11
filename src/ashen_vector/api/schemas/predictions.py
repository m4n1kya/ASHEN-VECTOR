"""Schemas for inference endpoints."""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class PredictionRequest(BaseModel):
    """Payload for requesting an inference."""
    symbol: str = Field(..., description="The symbol to predict")
    horizon: int = Field(5, description="Target horizon in days")
    classifier_id: str = Field(..., description="Model ID for classification")
    regressor_id: Optional[str] = Field(None, description="Model ID for regression (optional)")
    date: Optional[str] = Field(None, description="Specific date to predict for. Defaults to latest.")


class ModelInfo(BaseModel):
    id: str
    type: str
    version: str


class ModelsUsed(BaseModel):
    classification: ModelInfo
    regression: Optional[ModelInfo] = None


class PredictionOutput(BaseModel):
    status: Optional[str] = None
    direction: Optional[str] = None
    probability_up: Optional[float] = None
    probability_down: Optional[float] = None
    expected_return: Optional[float] = None


class ConfidenceScore(BaseModel):
    level: str
    score: int


class PredictionResponse(BaseModel):
    """Payload returned by the inference endpoint."""
    symbol: str
    date: str
    status: Optional[str] = None
    prediction: Optional[PredictionOutput] = None
    confidence: Optional[ConfidenceScore] = None
    models: Optional[ModelsUsed] = None
