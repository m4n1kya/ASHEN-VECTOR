"""
Overview Service orchestrating multiple backend services to deliver a unified dashboard payload.
"""
import math
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Tuple

from ashen_vector.config.settings import get_settings
from ashen_vector.data.instrument_service import InstrumentService
from ashen_vector.data.qlib_provider import get_provider
from ashen_vector.instruments.resolver import InstrumentResolver
from ashen_vector.features.pipeline import FeaturePipeline
from ashen_vector.analytics.statistics import compute_statistics
from ashen_vector.models.registry import ModelRegistry
from ashen_vector.predictions.engine import PredictionEngine

from ashen_vector.api.schemas.stocks import (
    StockOverviewResponse, MarketData, PerformanceData, RiskData,
    TechnicalData, PredictionData, ConfidenceData, SignalData, DataQuality
)

# Helper for NaN safety
def safe_float(val: Any) -> Any:
    if val is None:
        return None
    try:
        fval = float(val)
        if math.isnan(fval) or math.isinf(fval):
            return None
        return fval
    except:
        return None

class OverviewService:
    def __init__(self):
        self.provider = get_provider()
        self.instrument_service = InstrumentService(self.provider)
        self.resolver = InstrumentResolver(self.instrument_service)
        self.pipeline = FeaturePipeline(self.provider)
        self.registry = ModelRegistry()
        self.prediction_engine = PredictionEngine(self.registry, self.pipeline)
        self.settings = get_settings()
        
    def _get_trading_days_stale(self, latest_date: pd.Timestamp) -> int:
        """Calculate trading days stale relative to system time.
        Weekends (Saturday=5, Sunday=6) do not count as trading days.
        """
        now = pd.Timestamp.now().normalize()
        # pandas bdate_range computes business days between dates
        b_days = pd.bdate_range(start=latest_date, end=now)
        # subtract 1 because range is inclusive of start date
        days_stale = max(0, len(b_days) - 1)
        return days_stale
        
    def get_overview(self, symbol: str) -> StockOverviewResponse:
        # 1. Resolve Instrument
        # If this fails, it naturally throws InstrumentNotFoundError (404)
        instrument = self.resolver.resolve_exact(symbol)
        
        # We need historical data for Market, Perf, Risk, and Tech
        # Grab a generous window
        end_str = datetime.now().strftime("%Y-%m-%d")
        start_str = (pd.to_datetime(end_str) - pd.Timedelta(days=400)).strftime("%Y-%m-%d")
        
        try:
            df = self.provider.get_history(symbol, start_str, end_str)
            if df.empty:
                raise ValueError("Insufficient historical data")
        except Exception as e:
            # Let expected data errors bubble up or raise explicitly
            raise RuntimeError(f"Failed to fetch market data: {str(e)}")
            
        # Get actual dates from data
        latest_ts = df.index.max()
        if hasattr(latest_ts, '__len__') and len(latest_ts) == 2:
            latest_ts = latest_ts[1]
            
        latest_date_str = latest_ts.strftime("%Y-%m-%d")
        
        # Calculate staleness
        trading_days_stale = self._get_trading_days_stale(latest_ts)
        data_status = "STALE" if trading_days_stale > self.settings.stale_data_max_trading_days else "FRESH"
        
        # 2. Market Data
        # df has columns: $open, $high, $low, $close, $volume
        latest_row = df.iloc[-1]
        close_t = float(latest_row["$close"])
        close_t_1 = float(df.iloc[-2]["$close"]) if len(df) > 1 else close_t
        change_1d = (close_t - close_t_1) / close_t_1 if close_t_1 else 0.0
        
        market_data = MarketData(
            latest_date=latest_date_str,
            open=safe_float(latest_row["$open"]),
            high=safe_float(latest_row["$high"]),
            low=safe_float(latest_row["$low"]),
            close=safe_float(close_t),
            volume=safe_float(latest_row["$volume"]),
            change_1d=safe_float(change_1d)
        )
        
        # 3. Performance & Risk Data
        stats = compute_statistics(df["$close"])
        
        # Calculate periodic returns if we have enough days (approx 252 trading days/yr)
        def get_ret(days_back):
            if len(df) <= days_back: return None
            past_close = float(df.iloc[-(days_back+1)]["$close"])
            return (close_t - past_close) / past_close if past_close else None
            
        perf_data = PerformanceData(
            return_1d=safe_float(change_1d),
            return_1w=safe_float(get_ret(5)),
            return_1m=safe_float(get_ret(21)),
            return_3m=safe_float(get_ret(63)),
            return_6m=safe_float(get_ret(126)),
            return_1y=safe_float(get_ret(252)),
            return_ytd=None # Could compute YTD if needed
        )
        
        risk_data = RiskData(
            annualized_return=safe_float(stats.annualized_return),
            annualized_volatility=safe_float(stats.volatility_annualized),
            sharpe_ratio=safe_float(stats.sharpe_ratio),
            sortino_ratio=safe_float(stats.sortino_ratio),
            maximum_drawdown=safe_float(stats.max_drawdown),
            win_rate=safe_float(stats.win_rate),
            best_day=safe_float(stats.best_day),
            worst_day=safe_float(stats.worst_day)
        )
        
        # 4. Technicals & Data Quality via FeaturePipeline
        tech_data = TechnicalData()
        feat_df = self.pipeline.build_features(symbol, start_str, latest_date_str)
        
        feature_completeness = 0.0
        missing_features = []
        if not feat_df.empty:
            latest_feat = feat_df.iloc[-1]
            tech_data = TechnicalData(
                rsi_14=safe_float(latest_feat.get("rsi_14")),
                macd=safe_float(latest_feat.get("macd")),
                macd_signal=safe_float(latest_feat.get("macd_signal")),
                macd_histogram=safe_float(latest_feat.get("macd_hist")),
                sma_20=safe_float(latest_feat.get("sma_20")),
                sma_50=safe_float(latest_feat.get("sma_50")),
                sma_200=safe_float(latest_feat.get("sma_200")),
                ema_20=safe_float(latest_feat.get("ema_20")),
                momentum_20=safe_float(latest_feat.get("momentum_20")),
                volatility_20=safe_float(latest_feat.get("volatility_20")),
                volume_ratio_20=safe_float(latest_feat.get("volume_ratio_20")),
                bb_position=safe_float(latest_feat.get("bb_position")),
                bb_width=safe_float(latest_feat.get("bb_width")),
            )
            total_cols = len(latest_feat)
            nans = latest_feat.isna().sum()
            feature_completeness = (total_cols - nans) / total_cols
            missing_features = latest_feat[latest_feat.isna()].index.tolist()
            
        dq = DataQuality(
            latest_available_date=latest_date_str,
            data_status=data_status,
            trading_days_stale=trading_days_stale,
            feature_completeness=safe_float(feature_completeness),
            missing_features=missing_features,
            historical_observations=len(df)
        )
        
        # 5. Prediction
        pred_data = PredictionData(status="MODEL_UNAVAILABLE")
        conf_data = None
        sig_data = None
        models_data = None
        
        # Simple resolution for active models (in a real system, you'd lookup the registry index)
        cls_id = f"ashen_{symbol}_binary_{self.settings.default_horizon}d"
        reg_id = f"ashen_{symbol}_regression_{self.settings.default_horizon}d"
        
        try:
            # We don't predict on stale data by policy (can be overridden, but safe default)
            if data_status == "STALE":
                pred_data = PredictionData(status="MODEL_UNAVAILABLE_STALE_DATA")
            else:
                pred_result = self.prediction_engine.predict(
                    symbol=symbol,
                    horizon=self.settings.default_horizon,
                    classifier_id=cls_id,
                    regressor_id=reg_id,
                    date=latest_date_str
                )
                
                if pred_result.get("status") != "MODEL_UNAVAILABLE":
                    p = pred_result["prediction"]
                    pred_data = PredictionData(
                        status="ACTIVE",
                        direction=p.get("direction"),
                        probability_up=safe_float(p.get("probability_up")),
                        probability_down=safe_float(p.get("probability_down")),
                        expected_return=safe_float(p.get("expected_return"))
                    )
                    
                    if "confidence" in pred_result:
                        c = pred_result["confidence"]
                        conf_data = ConfidenceData(level=c.get("level"), score=c.get("score"))
                        
                    if "signal" in pred_result:
                        s = pred_result["signal"]
                        sig_data = SignalData(label=s.get("label"))
                        
                    models_data = pred_result.get("models")
        except Exception as e:
            # Prediction failures shouldn't kill the overview, but should be logged
            pred_data = PredictionData(status="PREDICTION_FAILED")
            
        return StockOverviewResponse(
            instrument=instrument,
            market=market_data,
            performance=perf_data,
            risk=risk_data,
            technical=tech_data,
            prediction=pred_data,
            confidence=conf_data,
            signal=sig_data,
            models=models_data,
            data_quality=dq,
            generated_at=datetime.utcnow().isoformat() + "Z"
        )
