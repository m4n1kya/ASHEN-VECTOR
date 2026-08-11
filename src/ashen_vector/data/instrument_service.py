"""Instrument service for ASHEN-VECTOR.

Handles symbol normalization, validation, search, and metadata retrieval.
Acts as the intermediary between user input and the Qlib data provider.
"""

import logging
from typing import Any

from ashen_vector.core.exceptions import InstrumentNotFoundError
from ashen_vector.data.qlib_provider import QlibProvider

logger = logging.getLogger(__name__)


class InstrumentService:
    """Service for finding, validating, and querying financial instruments."""

    def __init__(self, provider: QlibProvider) -> None:
        self._provider = provider

    # ------------------------------------------------------------------
    # Normalization
    # ------------------------------------------------------------------

    def normalize_symbol(self, raw: str) -> str:
        """Normalize a raw symbol string.

        Strips whitespace and converts to uppercase.
        """
        if not raw:
            return ""
        return raw.strip().upper()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_symbol(self, symbol: str) -> str:
        """Normalize and verify that the symbol exists in the dataset.

        Args:
            symbol: Raw user input symbol.

        Returns:
            Normalized symbol string.

        Raises:
            InstrumentNotFoundError: If the symbol does not exist.
        """
        normalized = self.normalize_symbol(symbol)
        if not normalized:
            raise InstrumentNotFoundError("")

        if not self._provider.instrument_exists(normalized):
            raise InstrumentNotFoundError(normalized)

        return normalized

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search_instruments(self, query: str) -> list[str]:
        """Search available instruments by prefix or substring match.

        Args:
            query: Search query (case-insensitive).

        Returns:
            List of matching instrument symbols.
        """
        normalized_query = self.normalize_symbol(query)
        all_instruments = self._provider.get_available_instruments()

        if not normalized_query:
            return all_instruments

        return [inst for inst in all_instruments if normalized_query in inst]

    # ------------------------------------------------------------------
    # Info
    # ------------------------------------------------------------------

    def get_instrument_info(self, symbol: str) -> dict[str, Any]:
        """Get metadata about an instrument including data coverage.

        Args:
            symbol: Instrument symbol (will be normalized).

        Returns:
            Dictionary with keys: symbol, available, data_start, data_end.

        Raises:
            InstrumentNotFoundError: If the symbol does not exist.
        """
        normalized = self.normalize_symbol(symbol)

        if not self._provider.instrument_exists(normalized):
            raise InstrumentNotFoundError(normalized)

        info: dict[str, Any] = {
            "symbol": normalized,
            "available": True,
            "data_start": None,
            "data_end": None,
        }

        try:
            # Fetch a wide date range to determine actual data coverage
            df = self._provider.get_history(
                normalized, "1990-01-01", "2030-12-31"
            )
            if df is not None and not df.empty:
                min_date = df.index.min()
                max_date = df.index.max()
                info["data_start"] = (
                    min_date.strftime("%Y-%m-%d")
                    if hasattr(min_date, "strftime")
                    else str(min_date)
                )
                info["data_end"] = (
                    max_date.strftime("%Y-%m-%d")
                    if hasattr(max_date, "strftime")
                    else str(max_date)
                )
        except Exception as exc:
            logger.warning(
                "Could not determine data coverage for %s: %s",
                normalized,
                exc,
            )

        return info
