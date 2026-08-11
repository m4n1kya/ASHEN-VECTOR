"""Exceptions module for ASHEN-VECTOR."""

from datetime import date
from typing import Union


class AshenVectorError(Exception):
    """Base exception for all ASHEN-VECTOR errors."""
    pass


class ConfigurationError(AshenVectorError):
    """Raised when there is a configuration issue."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class QlibProviderError(AshenVectorError):
    """Raised when there is an issue with Qlib initialization or data."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InstrumentNotFoundError(AshenVectorError):
    """Raised when an instrument does not exist in the dataset."""
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        super().__init__(f"Instrument not found in dataset: '{symbol}'")


class InsufficientDataError(AshenVectorError):
    """Raised when there is not enough data for calculation."""
    def __init__(self, symbol: str, required: int, available: int) -> None:
        self.symbol = symbol
        self.required = required
        self.available = available
        super().__init__(
            f"Insufficient data for '{symbol}'. Required: {required}, Available: {available}"
        )


class InvalidDateRangeError(AshenVectorError):
    """Raised when a bad date range is provided."""
    def __init__(self, start_date: Union[str, date], end_date: Union[str, date]) -> None:
        self.start_date = start_date
        self.end_date = end_date
        super().__init__(f"Invalid date range: {start_date} to {end_date}")


class ModelNotReadyError(AshenVectorError):
    """Raised when a model is accessed before it is trained or loaded."""
    def __init__(self, model_name: str = "Model") -> None:
        self.model_name = model_name
        super().__init__(f"{model_name} is not trained or ready yet.")


class FeatureComputationError(AshenVectorError):
    """Raised when feature computation fails."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class DataIntegrityError(AshenVectorError):
    """Raised when there is a data quality problem."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
