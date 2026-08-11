"""
Endpoints for model metadata.
"""
from fastapi import APIRouter, HTTPException

from ashen_vector.api.schemas.models import StockModelsResponse, ModelMetadata
from ashen_vector.models.registry import ModelRegistry
from ashen_vector.data.qlib_provider import get_provider
from ashen_vector.data.instrument_service import InstrumentService
from ashen_vector.core.exceptions import InstrumentNotFoundError

router = APIRouter(prefix="/stocks", tags=["models"])

def _get_instrument_service() -> InstrumentService:
    provider = get_provider()
    return InstrumentService(provider)

@router.get(
    "/{symbol}/models",
    response_model=StockModelsResponse,
    summary="Get available models for an instrument"
)
async def get_stock_models(symbol: str) -> StockModelsResponse:
    """Return list of available trained models and metadata for the instrument."""
    try:
        service = _get_instrument_service()
        validated_symbol = service.validate_symbol(symbol)
        
        registry = ModelRegistry()
        all_models = registry.list_models()
        
        # Filter models for this symbol
        models = []
        for model_id, meta in all_models.items():
            if f"_{validated_symbol}_" in model_id or meta.get("symbol") == validated_symbol:
                models.append(
                    ModelMetadata(
                        model_id=meta["model_id"],
                        type=meta["model_type"],
                        version=meta["model_version"],
                        target=meta["target"],
                        horizon=meta["horizon"],
                        validation=meta["validation"],
                        calibration=meta["calibration"],
                        status="ACTIVE", # or based on metrics/gate
                        metrics=meta.get("metrics", {})
                    )
                )
                
        return StockModelsResponse(symbol=validated_symbol, models=models)
        
    except InstrumentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
