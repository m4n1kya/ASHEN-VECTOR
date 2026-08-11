"""Stock data and instrument endpoints for ASHEN-VECTOR."""

from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from ashen_vector.core.exceptions import (
    InstrumentNotFoundError,
    QlibProviderError,
    InvalidDateRangeError,
)
from ashen_vector.data.qlib_provider import get_provider
from ashen_vector.data.instrument_service import InstrumentService

from ashen_vector.analytics.statistics import compute_statistics
from ashen_vector.features.pipeline import FeaturePipeline
from ashen_vector.data.schemas import AnalyticsResponse, FeatureResponse
import pandas as pd
import numpy as np
from ashen_vector.data.schemas import (
    StockHistoryResponse,
    OHLCVBar,
    InstrumentListResponse,
    InstrumentInfo,
    ErrorResponse,
)

router = APIRouter(tags=["stocks"])


def _get_instrument_service() -> InstrumentService:
    return InstrumentService(get_provider())


@router.get(
    "/instruments",
    response_model=InstrumentListResponse,
    summary="List available instruments",
)
async def list_instruments(
    query: Optional[str] = Query(None, alias="q", description="Search filter"),
    limit: int = Query(100, ge=1, le=1000),
) -> InstrumentListResponse:
    """List instruments available in the Qlib dataset."""
    try:
        service = _get_instrument_service()
        if query:
            instruments = service.search_instruments(query)
        else:
            instruments = get_provider().get_available_instruments()
        instruments = sorted(instruments)[:limit]
        return InstrumentListResponse(count=len(instruments), instruments=instruments)
    except QlibProviderError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get(
    "/instruments/{symbol}",
    response_model=InstrumentInfo,
    summary="Get instrument information",
    responses={404: {"model": ErrorResponse}},
)
async def get_instrument_info(symbol: str) -> InstrumentInfo:
    """Get detailed information about a specific instrument."""
    try:
        service = _get_instrument_service()
        info = service.get_instrument_info(symbol)
        return InstrumentInfo(**info)
    except InstrumentNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"{e.symbol} is not available in the current Qlib dataset.",
        )
    except QlibProviderError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get(
    "/stocks/{symbol}/history",
    response_model=StockHistoryResponse,
    summary="Get historical OHLCV data",
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}},
)
async def get_stock_history(
    symbol: str,
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    frequency: str = Query("day", description="Data frequency"),
) -> StockHistoryResponse:
    """Retrieve historical OHLCV data for an instrument."""
    # Validate date range
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail=f"start_date ({start_date}) must be before end_date ({end_date}).",
        )

    try:
        service = _get_instrument_service()
        validated_symbol = service.validate_symbol(symbol)

        provider = get_provider()
        df = provider.get_history(
            symbol=validated_symbol,
            start_date=str(start_date),
            end_date=str(end_date),
        )

        if df is None or df.empty:
            return StockHistoryResponse(
                symbol=validated_symbol,
                frequency=frequency,
                count=0,
                start_date=None,
                end_date=None,
                data=[],
            )

        # Convert DataFrame to response
        bars = []
        for idx, row in df.iterrows():
            # idx is a MultiIndex (instrument, datetime) from Qlib
            if hasattr(idx, '__len__') and len(idx) == 2:
                dt = idx[1]
            else:
                dt = idx
            bars.append(
                OHLCVBar(
                    date=str(dt.date()) if hasattr(dt, 'date') else str(dt),
                    open=round(float(row.iloc[0]), 6) if len(row) > 0 else 0.0,
                    high=round(float(row.iloc[1]), 6) if len(row) > 1 else 0.0,
                    low=round(float(row.iloc[2]), 6) if len(row) > 2 else 0.0,
                    close=round(float(row.iloc[3]), 6) if len(row) > 3 else 0.0,
                    volume=round(float(row.iloc[4]), 2) if len(row) > 4 else 0.0,
                )
            )

        return StockHistoryResponse(
            symbol=validated_symbol,
            frequency=frequency,
            count=len(bars),
            start_date=bars[0].date if bars else None,
            end_date=bars[-1].date if bars else None,
            data=bars,
        )

    except InstrumentNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"{e.symbol} is not available in the current Qlib dataset.",
        )
    except InvalidDateRangeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except QlibProviderError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error retrieving history: {type(e).__name__}"
        )

@router.get(
    "/stocks/{symbol}/analytics",
    response_model=AnalyticsResponse,
    summary="Get historical analytics"
)
async def get_analytics(
    symbol: str,
    start_date: Optional[str] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date YYYY-MM-DD")
) -> AnalyticsResponse:
    """Get financial statistics and performance metrics."""
    try:
        provider = get_provider()
        df = provider.get_history(symbol, start_date=start_date, end_date=end_date)
        if df.empty:
            return AnalyticsResponse(symbol=symbol, start_date=start_date, end_date=end_date)
            
        stats = compute_statistics(df["$close"])
        
        # Determine actual dates
        actual_start = df.index.min().strftime('%Y-%m-%d')
        actual_end = df.index.max().strftime('%Y-%m-%d')
        
        return AnalyticsResponse(
            symbol=symbol,
            start_date=actual_start,
            end_date=actual_end,
            latest_close=stats.latest_close,
            total_return=stats.total_return,
            annualized_return=stats.annualized_return,
            volatility=stats.volatility_daily,
            annualized_volatility=stats.volatility_annualized,
            sharpe_ratio=stats.sharpe_ratio,
            sortino_ratio=stats.sortino_ratio,
            maximum_drawdown=stats.max_drawdown,
            win_rate=stats.win_rate,
            average_positive_return=stats.avg_positive_return,
            average_negative_return=stats.avg_negative_return,
            best_day=stats.best_day,
            worst_day=stats.worst_day
        )
    except InstrumentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/stocks/{symbol}/features",
    response_model=FeatureResponse,
    summary="Get engineered features"
)
async def get_features(
    symbol: str,
    start_date: str = Query(..., description="Start date YYYY-MM-DD"),
    end_date: str = Query(..., description="End date YYYY-MM-DD")
) -> FeatureResponse:
    """Get ML features computed strictly without look-ahead bias."""
    try:
        provider = get_provider()
        pipeline = FeaturePipeline(provider)
        
        df = pipeline.build_features(symbol, start_date, end_date)
        
        if df.empty:
            return FeatureResponse(symbol=symbol, start_date=start_date, end_date=end_date, feature_count=0, features=[])
            
        df = df.reset_index()
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        elif 'index' in df.columns:
            df = df.rename(columns={'index': 'date'})
            
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        df = df.replace([np.nan], [None])
        
        features_list = df.to_dict(orient='records')
        feat_count = len([c for c in df.columns if c != 'date'])
        
        return FeatureResponse(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            feature_count=feat_count,
            features=features_list
        )
    except InstrumentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from ashen_vector.services.overview_service import OverviewService
from ashen_vector.api.schemas.stocks import StockOverviewResponse, LatestFeatureResponse

@router.get(
    "/stocks/{symbol}/overview",
    response_model=StockOverviewResponse,
    summary="Get unified dashboard overview"
)
async def get_overview(symbol: str) -> StockOverviewResponse:
    """Aggregates all market, feature, prediction, and analytics data."""
    try:
        service = OverviewService()
        return service.get_overview(symbol)
    except InstrumentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    # Note: We purposely do NOT catch Exception here to avoid swallowing errors 
    # except those intentionally raised as 404/400.

@router.get(
    "/stocks/{symbol}/features/latest",
    response_model=LatestFeatureResponse,
    summary="Get the latest inference feature vector"
)
async def get_latest_features(symbol: str) -> LatestFeatureResponse:
    try:
        provider = get_provider()
        pipeline = FeaturePipeline(provider)
        
        import datetime
        import pandas as pd
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        start_date = (pd.to_datetime(end_date) - pd.Timedelta(days=50)).strftime("%Y-%m-%d")
        
        df = pipeline.build_features(symbol, start_date, end_date)
        if df.empty:
            raise HTTPException(status_code=404, detail="No features available.")
            
        latest = df.iloc[-1]
        
        # Format the date nicely if it's a timestamp
        target_date = latest.name
        if hasattr(target_date, "strftime"):
            target_date = target_date.strftime("%Y-%m-%d")
        elif hasattr(target_date, "__len__") and len(target_date) == 2:
            target_date = target_date[1].strftime("%Y-%m-%d") # MultiIndex
        else:
            target_date = str(target_date)
            
        # Convert NaN to None for JSON compliance
        feats = {k: (None if pd.isna(v) else float(v)) for k, v in latest.items()}
        
        return LatestFeatureResponse(
            symbol=symbol,
            date=target_date,
            features=feats
        )
    except InstrumentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
