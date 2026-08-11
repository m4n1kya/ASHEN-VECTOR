"""
Instrument search API schemas.
"""
from pydantic import BaseModel, Field
from typing import List
from ashen_vector.instruments.schemas import Instrument

class InstrumentSearchResponse(BaseModel):
    """Response model for instrument search."""
    query: str
    results: List[Instrument]
    count: int = Field(..., description="Number of results found")
