"""Health check endpoint for ASHEN-VECTOR."""

from fastapi import APIRouter

from ashen_vector import __version__, __application__
from ashen_vector.config.settings import get_settings
from ashen_vector.data.qlib_provider import get_provider
from ashen_vector.data.schemas import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """System health check including Qlib and model status."""
    settings = get_settings()
    provider = get_provider()

    # Qlib status
    if provider.is_initialized():
        qlib_status = {
            "status": "ready",
            "provider": str(settings.qlib_provider_uri),
            "region": settings.qlib_region,
        }
    else:
        qlib_status = {
            "status": "not_initialized",
            "provider": str(settings.qlib_provider_uri),
        }

    # Model status (Phase 1: no models yet)
    model_status = {
        "status": "not_initialized",
        "message": "No trained models available. Use the training pipeline to create models.",
    }

    return HealthResponse(
        status="healthy" if provider.is_initialized() else "degraded",
        application=__application__,
        version=__version__,
        qlib=qlib_status,
        models=model_status,
    )
