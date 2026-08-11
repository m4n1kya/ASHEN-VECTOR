from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings for ASHEN-VECTOR."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "ASHEN-VECTOR"
    app_env: str = "development"
    debug: bool = False
    api_prefix: str = "/api"

    # Qlib
    qlib_provider_uri: str = "../qlib/qlib_bin"
    qlib_region: str = "us"

    # Directories
    model_dir: str = "./artifacts/models"
    cache_dir: str = "./artifacts/cache"
    log_dir: str = "./logs"

    # API
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    # Prediction defaults
    default_horizon: int = 5
    stale_data_max_trading_days: int = 5
    
    # Data safety
    forbidden_inference_columns: set = {
        "future_direction",
        "future_return",
        "future_return_1d",
        "future_return_5d",
        "future_return_10d",
        "future_return_20d",
        "future_close",
        "label",
        "target"
    }

    @property
    def resolved_qlib_uri(self) -> Path:
        """Resolve the Qlib provider URI relative to the project root."""
        uri_path = Path(self.qlib_provider_uri)
        if uri_path.is_absolute():
            return uri_path
        # Resolve relative to the project root (where pyproject.toml lives)
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        return (project_root / uri_path).resolve()

    @property
    def is_development(self) -> bool:
        """Check if the application is running in development environment."""
        return self.app_env == "development"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached application settings singleton."""
    return Settings()
