from fastapi import APIRouter, HTTPException, Depends
from ashen_vector.api.services.live_market import LiveMarketService, LiveAnalysisRequest

router = APIRouter()

def get_live_service():
    return LiveMarketService()

@router.post("/analyze")
async def analyze_live_ticker(
    request: LiveAnalysisRequest,
    service: LiveMarketService = Depends(get_live_service)
):
    try:
        result = service.analyze(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
