"""ASHEN-VECTOR API — Main application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ashen_vector import __version__, __application__
from ashen_vector.config.settings import get_settings
from ashen_vector.data.qlib_provider import get_provider
from ashen_vector.api.routes import health, stocks, predictions, training, instruments, models, backtest


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize resources on startup."""
    settings = get_settings()
    provider = get_provider()
    try:
        provider.initialize()
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(
            f"Qlib initialization failed during startup: {e}. "
            "Some endpoints will be unavailable."
        )
    yield
    # Cleanup if needed


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Quantitative Market Intelligence Platform",
        version=__version__,
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        lifespan=lifespan,
    )

    # CORS middleware for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(instruments.router, prefix=settings.api_prefix)
    app.include_router(stocks.router, prefix=settings.api_prefix)
    app.include_router(predictions.router, prefix=settings.api_prefix)
    app.include_router(training.router, prefix=settings.api_prefix)
    app.include_router(models.router, prefix=settings.api_prefix)
    app.include_router(backtest.router, prefix=settings.api_prefix)


    return app


app = create_app()
