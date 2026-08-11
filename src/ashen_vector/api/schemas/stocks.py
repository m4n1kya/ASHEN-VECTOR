"""
Unified Overview and Stock endpoints schemas.
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from ashen_vector.instruments.schemas import Instrument

class MarketData(BaseModel):
    latest_date: str
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None
    change_1d: Optional[float] = None

class PerformanceData(BaseModel):
    return_1d: Optional[float] = None
    return_1w: Optional[float] = None
    return_1m: Optional[float] = None
    return_3m: Optional[float] = None
    return_6m: Optional[float] = None
    return_1y: Optional[float] = None
    return_ytd: Optional[float] = None

class RiskData(BaseModel):
    annualized_return: Optional[float] = None
    annualized_volatility: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    maximum_drawdown: Optional[float] = None
    win_rate: Optional[float] = None
    best_day: Optional[float] = None
    worst_day: Optional[float] = None

class TechnicalData(BaseModel):
    rsi_14: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_20: Optional[float] = None
    momentum_20: Optional[float] = None
    volatility_20: Optional[float] = None
    volume_ratio_20: Optional[float] = None
    bb_position: Optional[float] = None
    bb_width: Optional[float] = None

class PredictionData(BaseModel):
    status: str
    direction: Optional[str] = None
    probability_up: Optional[float] = None
    probability_down: Optional[float] = None
    expected_return: Optional[float] = None

class ConfidenceData(BaseModel):
    level: Optional[str] = None
    score: Optional[int] = None

class SignalData(BaseModel):
    label: Optional[str] = None
    type: str = "QUANTITATIVE_MODEL_SIGNAL"

class DataQuality(BaseModel):
    latest_available_date: str
    data_status: str
    trading_days_stale: int
    feature_completeness: Optional[float] = None
    missing_features: List[str] = []
    historical_observations: Optional[int] = None

class StockOverviewResponse(BaseModel):
    """Primary endpoint response for dashboard consumption."""
    instrument: Instrument
    market: MarketData
    performance: PerformanceData
    risk: RiskData
    technical: TechnicalData
    prediction: PredictionData
    confidence: Optional[ConfidenceData] = None
    signal: Optional[SignalData] = None
    models: Optional[Dict[str, Any]] = None
    data_quality: DataQuality
    generated_at: str

class LatestFeatureResponse(BaseModel):
    symbol: str
    date: str
    features: Dict[str, Optional[float]]
