"""
Instrument resolution schemas.
"""
from pydantic import BaseModel
from typing import Optional

class Instrument(BaseModel):
    """Canonical instrument object."""
    symbol: str
    name: str
    exchange: str
    asset_type: str
