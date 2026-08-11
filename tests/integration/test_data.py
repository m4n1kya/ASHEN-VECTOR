"""ASHEN-VECTOR Integration Tests — Data Layer.

Tests that verify the Qlib data provider works correctly with
the configured dataset. These tests require a valid Qlib binary
dataset to be available at the configured provider URI.
"""

import sys
from pathlib import Path

import pytest

# Ensure src is on path for test discovery
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))


@pytest.fixture(scope="module")
def provider():
    """Get an initialized QlibProvider instance."""
    from ashen_vector.data.qlib_provider import get_provider

    p = get_provider()
    p.initialize()
    return p


@pytest.fixture(scope="module")
def instrument_service(provider):
    """Get an InstrumentService instance."""
    from ashen_vector.data.instrument_service import InstrumentService

    return InstrumentService(provider)


# ---------------------------------------------------------------------------
# Qlib Initialization
# ---------------------------------------------------------------------------


class TestQlibInitialization:
    """Tests for Qlib provider initialization."""

    def test_provider_initializes(self, provider):
        """Qlib should initialize without errors."""
        assert provider.is_initialized()

    def test_provider_is_singleton(self):
        """get_provider() should return the same instance."""
        from ashen_vector.data.qlib_provider import get_provider

        p1 = get_provider()
        p2 = get_provider()
        assert p1 is p2


# ---------------------------------------------------------------------------
# Instrument Discovery
# ---------------------------------------------------------------------------


class TestInstrumentDiscovery:
    """Tests for instrument listing and existence checks."""

    def test_instruments_available(self, provider):
        """At least one instrument should be available."""
        instruments = provider.get_available_instruments()
        assert len(instruments) > 0

    def test_sh600000_exists(self, provider):
        """SH600000 should exist in the dataset."""
        assert provider.instrument_exists("SH600000")

    def test_nonexistent_instrument(self, provider):
        """A fabricated symbol should not exist."""
        assert not provider.instrument_exists("ZZZZZ_FAKE_99999")

    def test_instrument_search(self, instrument_service):
        """Search should find SH600000 when querying 'SH600'."""
        results = instrument_service.search_instruments("SH600")
        assert any("SH600000" in r for r in results)


# ---------------------------------------------------------------------------
# Symbol Validation
# ---------------------------------------------------------------------------


class TestSymbolValidation:
    """Tests for symbol normalization and validation."""

    def test_normalize_whitespace(self, instrument_service):
        """Symbol should be trimmed and uppercased."""
        normalized = instrument_service.normalize_symbol("  sh600000  ")
        assert normalized == "SH600000"

    def test_validate_valid_symbol(self, instrument_service):
        """Validating an existing symbol should return the normalized form."""
        result = instrument_service.validate_symbol("sh600000")
        assert result == "SH600000"

    def test_validate_invalid_symbol(self, instrument_service):
        """Validating a non-existent symbol should raise InstrumentNotFoundError."""
        from ashen_vector.core.exceptions import InstrumentNotFoundError

        with pytest.raises(InstrumentNotFoundError):
            instrument_service.validate_symbol("ZZZZZ_FAKE_99999")


# ---------------------------------------------------------------------------
# Historical Data Retrieval
# ---------------------------------------------------------------------------


class TestHistoricalData:
    """Tests for OHLCV data retrieval."""

    def test_sh600000_ohlcv(self, provider):
        """SH600000 should return OHLCV data for a known date range."""
        df = provider.get_history(
            symbol="SH600000",
            start_date="2020-01-01",
            end_date="2020-01-10",
        )
        assert df is not None
        assert not df.empty
        # Should have 5 columns: open, high, low, close, volume
        assert df.shape[1] == 5

    def test_ohlcv_columns_present(self, provider):
        """Returned DataFrame should have the expected columns."""
        df = provider.get_history(
            symbol="SH600000",
            start_date="2020-01-01",
            end_date="2020-01-10",
        )
        # Column names from Qlib include the $ prefix
        col_names = [c.lower() for c in df.columns]
        for expected in ["open", "high", "low", "close", "volume"]:
            assert any(expected in c for c in col_names), (
                f"Expected column containing '{expected}' not found in {col_names}"
            )

    def test_ohlcv_data_integrity(self, provider):
        """OHLC relationship: high >= low for each bar."""
        df = provider.get_history(
            symbol="SH600000",
            start_date="2020-01-01",
            end_date="2020-12-31",
        )
        if df is not None and not df.empty:
            # Columns may be named $high/$low or similar
            high_col = [c for c in df.columns if "high" in c.lower()][0]
            low_col = [c for c in df.columns if "low" in c.lower()][0]
            assert (df[high_col] >= df[low_col]).all(), "High should be >= Low for all bars"

    def test_empty_result_for_future_dates(self, provider):
        """Requesting data far in the future should return empty or None."""
        df = provider.get_history(
            symbol="SH600000",
            start_date="2090-01-01",
            end_date="2090-12-31",
        )
        assert df is None or df.empty

    def test_invalid_symbol_raises(self, provider):
        """Getting history for a non-existent symbol should return empty."""
        df = provider.get_history(
            symbol="ZZZZZ_FAKE_99999",
            start_date="2020-01-01",
            end_date="2020-01-10",
        )
        # Qlib may return empty DataFrame or raise; we handle both
        assert df is None or df.empty


# ---------------------------------------------------------------------------
# Instrument Info
# ---------------------------------------------------------------------------


class TestInstrumentInfo:
    """Tests for instrument information retrieval."""

    def test_instrument_info_sh600000(self, instrument_service):
        """Should return valid info for SH600000."""
        info = instrument_service.get_instrument_info("SH600000")
        assert info["symbol"] == "SH600000"
        assert info["available"] is True

    def test_instrument_info_unavailable(self, instrument_service):
        """Should indicate unavailable for non-existent symbol."""
        from ashen_vector.core.exceptions import InstrumentNotFoundError

        with pytest.raises(InstrumentNotFoundError):
            instrument_service.get_instrument_info("ZZZZZ_FAKE_99999")
