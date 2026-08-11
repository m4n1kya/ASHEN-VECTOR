"""
Pydantic schemas for the data API.
"""

from typing import Any
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any

class OHLCVBar(BaseModel):
    """OHLCV data for a single bar/day."""
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float

class StockHistoryResponse(BaseModel):
    """Response model for historical stock data."""
    symbol: str
    frequency: str
    count: int
    start_date: Optional[str]
    end_date: Optional[str]
    data: List[OHLCVBar]
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "symbol": "AAPL",
                "frequency": "day",
                "count": 1,
                "start_date": "2023-01-01",
                "end_date": "2023-01-01",
                "data": [{
                    "date": "2023-01-01",
                    "open": 150.0,
                    "high": 155.0,
                    "low": 149.0,
                    "close": 153.0,
                    "volume": 1000000.0
                }]
            }
        }
    )

class InstrumentInfo(BaseModel):
    """Information about a specific instrument."""
    symbol: str
    available: bool
    data_start: Optional[str] = None
    data_end: Optional[str] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "symbol": "AAPL",
                "available": True,
                "data_start": "2010-01-01",
                "data_end": "2023-12-31"
            }
        }
    )

class InstrumentListResponse(BaseModel):
    """Response model for a list of instruments."""
    count: int
    instruments: List[str]
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count": 2,
                "instruments": ["AAPL", "MSFT"]
            }
        }
    )

class HealthResponse(BaseModel):
    """Response model for API health check."""
    status: str
    application: str
    version: str
    qlib: Dict[str, Any]
    models: Dict[str, Any]

class ErrorResponse(BaseModel):
    """Response model for API errors."""
    error: str
    detail: Optional[str] = None
    symbol: Optional[str] = None

class AnalyticsResponse(BaseModel):
    """Response model for stock analytics statistics."""
    symbol: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    latest_date: str
    latest_close: float
    daily_return: Optional[float] = None
    weekly_return: Optional[float] = None
    monthly_return: Optional[float] = None
    total_return: Optional[float] = None
    annualized_return: Optional[float] = None
    volatility_daily: Optional[float] = None
    volatility_annualized: Optional[float] = None
    max_drawdown: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    win_rate: Optional[float] = None
    avg_positive_return: Optional[float] = None
    avg_negative_return: Optional[float] = None
    best_day: Optional[float] = None
    worst_day: Optional[float] = None
    high_52w: Optional[float] = None
    low_52w: Optional[float] = None
    distance_from_52w_high: Optional[float] = None
    distance_from_52w_low: Optional[float] = None
    total_trading_days: int

class FeatureResponse(BaseModel):
    """Response model for stock features."""
    symbol: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    feature_count: int
    features: List[Dict[str, Any]]


class AnalyticsResponse(BaseModel):
    symbol: str
    start_date: str | None
    end_date: str | None
    latest_close: float | None = None
    total_return: float | None = None
    annualized_return: float | None = None
    volatility: float | None = None
    annualized_volatility: float | None = None
    sharpe_ratio: float | None = None
    sortino_ratio: float | None = None
    maximum_drawdown: float | None = None
    win_rate: float | None = None
    average_positive_return: float | None = None
    average_negative_return: float | None = None
    best_day: float | None = None
    worst_day: float | None = None


class FeatureResponse(BaseModel):
    symbol: str
    start_date: str | None
    end_date: str | None
    feature_count: int
    features: list[dict[str, Any]]
