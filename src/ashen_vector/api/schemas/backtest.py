"""
Backtest API schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class BacktestRequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    horizon: int = Field(default=5, ge=1)
    initial_capital: float = Field(default=100000.0, ge=0.0)
    strategy: str = Field(default="ashen_vector")
    commission_bps: int = Field(default=5, ge=0)
    slippage_bps: int = Field(default=5, ge=0)

class BacktestResponse(BaseModel):
    status: str
    message: Optional[str] = None
    strategy: Optional[str] = None
    period: Optional[Dict[str, str]] = None
    performance: Optional[Dict[str, float]] = None
    costs: Optional[Dict[str, float]] = None

class BacktestJobStatus(BaseModel):
    job_id: str
    status: str
    submitted_at: float
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    error: Optional[str] = None

class BenchmarkComparison(BaseModel):
    buy_and_hold: Dict[str, Any]
    momentum: Dict[str, Any]
    sma20: Dict[str, Any]
    verdict: str

class BacktestResult(BaseModel):
    predictive_performance: Dict[str, float]
    trading_performance: Dict[str, float]
    risk_metrics: Dict[str, float]
    benchmark_comparison: BenchmarkComparison
