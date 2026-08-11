"""
Backtest API routes.
Handles running backtests asynchronously and checking status.
"""
from fastapi import APIRouter, HTTPException

from ashen_vector.api.schemas.backtest import (
    BacktestRequest, BacktestJobStatus, BacktestResult, BacktestResponse
)
from ashen_vector.backtesting.job_manager import job_manager
from ashen_vector.backtesting.runner import run_full_backtest
from ashen_vector.data.qlib_provider import get_provider
from ashen_vector.features.pipeline import FeaturePipeline
from ashen_vector.data.instrument_service import InstrumentService
from ashen_vector.core.exceptions import InstrumentNotFoundError

router = APIRouter(tags=["backtest"])

def _get_instrument_service() -> InstrumentService:
    return InstrumentService(get_provider())

@router.get(
    "/stocks/{symbol}/backtest",
    response_model=BacktestResponse,
    summary="Get backtest results for an instrument (Stub for historical)"
)
async def get_backtest(symbol: str) -> BacktestResponse:
    try:
        service = _get_instrument_service()
        service.validate_symbol(symbol)
        
        return BacktestResponse(
            status="NOT_AVAILABLE",
            message="Backtesting results are not yet available for this instrument."
        )
    except InstrumentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/backtest/run", response_model=BacktestJobStatus)
async def submit_backtest(request: BacktestRequest) -> BacktestJobStatus:
    try:
        service = _get_instrument_service()
        service.validate_symbol(request.symbol)
    except InstrumentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    pipeline = FeaturePipeline(get_provider())
    
    job_id = job_manager.submit_job(
        run_full_backtest,
        symbol=request.symbol,
        start_date=request.start_date,
        end_date=request.end_date,
        horizon=request.horizon,
        initial_capital=request.initial_capital,
        strategy_name=request.strategy,
        commission_bps=request.commission_bps,
        slippage_bps=request.slippage_bps,
        pipeline=pipeline
    )
    
    job = job_manager.get_job(job_id)
    return BacktestJobStatus(**job)

@router.get("/backtest/jobs/{job_id}", response_model=BacktestJobStatus)
async def get_job_status(job_id: str) -> BacktestJobStatus:
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    # Create safe copy without traceback for status response
    safe_job = {k: v for k, v in job.items() if k not in ["result", "traceback"]}
    if "traceback" in job and job["traceback"]:
        safe_job["error"] = job["error"] # Keep brief error message
        
    return BacktestJobStatus(**safe_job)

@router.get("/backtest/jobs/{job_id}/result", response_model=BacktestResult)
async def get_job_result(job_id: str) -> BacktestResult:
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job["status"] == "FAILED":
        error_msg = f"{job.get('error', 'Unknown error')}\n\nTraceback:\n{job.get('traceback', '')}"
        raise HTTPException(status_code=500, detail=error_msg)
        
    if job["status"] != "COMPLETED":
        raise HTTPException(status_code=400, detail="Job is not completed yet")
        
    return BacktestResult(**job["result"])
