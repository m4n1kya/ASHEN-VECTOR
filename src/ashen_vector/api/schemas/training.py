"""Schemas for training endpoints."""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class TrainingRequest(BaseModel):
    """Payload for starting a training job."""
    symbol: str = Field(..., description="The symbol to train on")
    start_date: str = Field(..., description="Start date for training data (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date for training data (YYYY-MM-DD)")
    model_type: str = Field("lightgbm", description="Model type (lightgbm, random_forest)")
    objective: str = Field("binary", description="binary or regression")
    target_col: str = Field("future_direction", description="Target column to predict")
    horizon: int = Field(5, description="Target horizon in days")
    model_kwargs: Dict[str, Any] = Field(default_factory=dict, description="Model hyperparameters")


class JobResponse(BaseModel):
    """Response when a job is queued."""
    job_id: str
    status: str
    message: str


class JobStatusResponse(BaseModel):
    """Response when checking a job status."""
    job_id: str
    status: str
    result: Optional[str] = None
    model_id: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    baseline: Optional[Dict[str, Any]] = None
    reason: Optional[str] = None
    error: Optional[str] = None
