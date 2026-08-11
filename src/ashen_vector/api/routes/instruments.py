"""
Endpoints for instrument search and metadata.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ashen_vector.api.schemas.instruments import InstrumentSearchResponse
from ashen_vector.instruments.resolver import InstrumentResolver
from ashen_vector.data.instrument_service import InstrumentService
from ashen_vector.data.qlib_provider import get_provider

router = APIRouter(prefix="/instruments", tags=["instruments"])

def get_resolver() -> InstrumentResolver:
    provider = get_provider()
    service = InstrumentService(provider)
    return InstrumentResolver(service)

@router.get("/search", response_model=InstrumentSearchResponse, summary="Search available instruments")
async def search_instruments(
    q: str = Query(..., description="Search query (symbol or name)"),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Search for instruments in the backend dataset.
    Matches symbols and known company metadata safely.
    """
    try:
        resolver = get_resolver()
        results = resolver.search(q)
        results = results[:limit]
        return InstrumentSearchResponse(query=q, results=results, count=len(results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
