from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from ashen_vector.backtesting.job_manager import job_manager
from ashen_vector.api.services.validation_runner import run_validation_job

router = APIRouter(tags=["validation"])

class ValidationRequest(BaseModel):
    symbol: str
    model: str
    horizon: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    purge_window: int = 5
    embargo_window: int = 5
    n_splits: int = 5

class ValidationJobStatus(BaseModel):
    job_id: str
    status: str
    progress: float = 0.0
    message: str = ""
    error: Optional[str] = None

@router.post("/validation/run", response_model=ValidationJobStatus)
async def submit_validation(request: ValidationRequest) -> ValidationJobStatus:
    try:
        job_id = job_manager.submit_job(
            run_validation_job,
            symbol=request.symbol,
            model_name=request.model,
            horizon=request.horizon,
            start_date=request.start_date,
            end_date=request.end_date,
            purge_window=request.purge_window,
            embargo_window=request.embargo_window,
            n_splits=request.n_splits
        )
        job = job_manager.get_job(job_id)
        return ValidationJobStatus(
            job_id=job["id"],
            status=job["status"],
            progress=job.get("progress", 0.0),
            message=job.get("message", ""),
            error=job.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/validation/jobs/{job_id}", response_model=ValidationJobStatus)
async def get_job_status(job_id: str) -> ValidationJobStatus:
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return ValidationJobStatus(
        job_id=job["id"],
        status=job["status"],
        progress=job.get("progress", 0.0),
        message=job.get("message", ""),
        error=job.get("error", "Unknown error") if job.get("traceback") else job.get("error")
    )

@router.get("/validation/jobs/{job_id}/results")
async def get_job_result(job_id: str) -> Dict[str, Any]:
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job["status"] == "FAILED":
        raise HTTPException(status_code=500, detail=job.get('error', 'Unknown error'))
        
    if job["status"] != "COMPLETED":
        raise HTTPException(status_code=400, detail="Job is not completed yet")
        
    return job["result"]
