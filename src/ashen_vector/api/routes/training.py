"""
Endpoints for training models asynchronously.
"""
import uuid
import asyncio
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks

from ashen_vector.api.schemas.training import TrainingRequest, JobResponse, JobStatusResponse
from ashen_vector.data.qlib_provider import get_provider
from ashen_vector.features.pipeline import FeaturePipeline
from ashen_vector.models.registry import ModelRegistry, MODEL_TYPES
from ashen_vector.models.trainer import ModelTrainer

router = APIRouter(prefix="/training", tags=["training"])

# In-memory job store for Phase 3 (in prod, use Redis/DB)
TRAINING_JOBS: Dict[str, Dict[str, Any]] = {}

def get_trainer() -> ModelTrainer:
    provider = get_provider()
    pipeline = FeaturePipeline(provider)
    registry = ModelRegistry()
    return ModelTrainer(pipeline, registry)

def _run_training_task(job_id: str, request: TrainingRequest):
    """Background task to run the training pipeline."""
    try:
        trainer = get_trainer()
        
        if request.model_type not in MODEL_TYPES:
            TRAINING_JOBS[job_id] = {
                "job_id": job_id,
                "status": "failed",
                "error": f"Unknown model_type {request.model_type}"
            }
            return
            
        model_cls = MODEL_TYPES[request.model_type]
        
        result = trainer.run_training_job(
            job_id=job_id,
            symbol=request.symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            model_cls=model_cls,
            model_kwargs=request.model_kwargs,
            objective=request.objective,
            target_col=request.target_col,
            horizon=request.horizon
        )
        
        TRAINING_JOBS[job_id] = result
        
    except Exception as e:
        TRAINING_JOBS[job_id] = {
            "job_id": job_id,
            "status": "failed",
            "error": str(e)
        }

@router.post("/train", response_model=JobResponse, summary="Start an asynchronous training job")
async def start_training(request: TrainingRequest, background_tasks: BackgroundTasks):
    job_id = f"train_{uuid.uuid4().hex[:8]}"
    
    TRAINING_JOBS[job_id] = {
        "job_id": job_id,
        "status": "running"
    }
    
    background_tasks.add_task(_run_training_task, job_id, request)
    
    return JobResponse(
        job_id=job_id,
        status="queued",
        message="Training job has been queued in the background."
    )

@router.get("/jobs/{job_id}", response_model=JobStatusResponse, summary="Get training job status")
async def get_job_status(job_id: str):
    if job_id not in TRAINING_JOBS:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return JobStatusResponse(**TRAINING_JOBS[job_id])
    
@router.get("/models", summary="List all trained models")
async def list_models():
    registry = ModelRegistry()
    return registry.list_models()
