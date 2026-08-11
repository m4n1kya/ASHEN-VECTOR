"""Qlib data provider for ASHEN-VECTOR.

This module is the ONLY place responsible for initializing Microsoft Qlib
and providing data access. All other modules should use this provider
rather than importing Qlib directly.

Thread-safe singleton — Qlib is initialized once and reused.
"""

import logging
import threading
from pathlib import Path
from typing import Optional

import pandas as pd

from ashen_vector.core.exceptions import InstrumentNotFoundError, QlibProviderError

logger = logging.getLogger(__name__)


class QlibProvider:
    """Thread-safe singleton provider for Microsoft Qlib data access.

    Usage:
        provider = get_provider()
        provider.initialize()
        df = provider.get_history("SH600000", "2020-01-01", "2020-12-31")
    """

    _instance: Optional["QlibProvider"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "QlibProvider":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._initialized = False
                    instance._init_lock = threading.Lock()
                    cls._instance = instance
        return cls._instance

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """Initialize Qlib with the configured provider URI.

        Safe to call multiple times — only the first call performs initialization.
        Raises QlibProviderError if initialization fails.
        """
        if self._initialized:
            return

        with self._init_lock:
            if self._initialized:
                return

            from ashen_vector.config.settings import get_settings

            settings = get_settings()
            resolved_uri = settings.resolved_qlib_uri

            if not resolved_uri.exists():
                raise QlibProviderError(
                    f"Qlib provider URI does not exist: {resolved_uri}. "
                    f"Configured as: {settings.qlib_provider_uri}"
                )

            try:
                import qlib

                logger.info(
                    "Initializing Qlib — provider_uri=%s, region=%s",
                    resolved_uri,
                    settings.qlib_region,
                )
                qlib.init(
                    provider_uri=str(resolved_uri),
                    region=settings.qlib_region,
                )
                self._initialized = True
                logger.info("Qlib initialized successfully.")
            except ImportError as exc:
                raise QlibProviderError(
                    "Qlib is not installed. Install it with: pip install -e ../qlib"
                ) from exc
            except Exception as exc:
                raise QlibProviderError(
                    f"Failed to initialize Qlib: {exc}"
                ) from exc

    def is_initialized(self) -> bool:
        """Check whether Qlib has been successfully initialized."""
        return getattr(self, "_initialized", False)

    # ------------------------------------------------------------------
    # Data Access
    # ------------------------------------------------------------------

    def get_history(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        fields: Optional[list[str]] = None,
    ) -> pd.DataFrame:
        """Retrieve historical OHLCV data for a single instrument.

        Args:
            symbol: Instrument identifier (e.g. "SH600000").
            start_date: Start date string (YYYY-MM-DD).
            end_date: End date string (YYYY-MM-DD).
            fields: Qlib feature fields. Defaults to OHLCV.

        Returns:
            DataFrame indexed by datetime with columns for each field.
            Returns an empty DataFrame if no data is available.
        """
        if not self.is_initialized():
            self.initialize()

        if fields is None:
            fields = ["$open", "$high", "$low", "$close", "$volume"]

        try:
            from qlib.data import D

            df = D.features(
                [symbol],
                fields,
                start_time=start_date,
                end_time=end_date,
            )

            if df is None or df.empty:
                return pd.DataFrame(columns=fields)

            # Qlib returns MultiIndex (instrument, datetime) — drop instrument level
            if df.index.nlevels > 1:
                df = df.droplevel("instrument")

            return df

        except Exception as exc:
            error_msg = str(exc).lower()
            if "not found" in error_msg or "cannot find" in error_msg:
                raise InstrumentNotFoundError(symbol) from exc
            logger.error("Error fetching history for %s: %s", symbol, exc)
            raise QlibProviderError(
                f"Failed to fetch history for {symbol}: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Instrument Discovery
    # ------------------------------------------------------------------

    def get_available_instruments(self) -> list[str]:
        """List all instruments available in the configured Qlib dataset.

        Discovers instruments by scanning the features/ subdirectory
        of the provider URI, since each instrument has its own folder.

        Returns:
            Sorted list of instrument symbols (uppercased).
        """
        from ashen_vector.config.settings import get_settings

        settings = get_settings()
        features_dir = settings.resolved_qlib_uri / "features"

        if not features_dir.exists() or not features_dir.is_dir():
            logger.warning("Features directory not found at %s", features_dir)
            return []

        try:
            instruments = sorted(
                entry.name.upper()
                for entry in features_dir.iterdir()
                if entry.is_dir()
            )
            return instruments
        except Exception as exc:
            logger.error("Error listing instruments: %s", exc)
            raise QlibProviderError(f"Failed to list instruments: {exc}") from exc

    def instrument_exists(self, symbol: str) -> bool:
        """Check whether an instrument exists in the Qlib dataset.

        Args:
            symbol: Instrument identifier (case-insensitive).

        Returns:
            True if the instrument's feature directory exists.
        """
        from ashen_vector.config.settings import get_settings

        settings = get_settings()
        features_dir = settings.resolved_qlib_uri / "features"
        # Qlib stores feature directories in lowercase
        instrument_dir = features_dir / symbol.lower()
        return instrument_dir.exists() and instrument_dir.is_dir()


def get_provider() -> QlibProvider:
    """Get the singleton QlibProvider instance."""
    return QlibProvider()
