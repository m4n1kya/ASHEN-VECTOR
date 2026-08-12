import asyncio
from ashen_vector.api.services.live_market import LiveMarketService, LiveAnalysisRequest

async def run():
    srv = LiveMarketService()
    req = LiveAnalysisRequest(symbol="AAPL", models=["MOMENTUM", "MEAN REVERSION", "LIGHTGBM"], horizons=[21])
    res = srv.analyze(req)
    print("ARS SCORE:", res["reliability_score"])
    print("ARS COMPONENTS:", res["ars_components"])
    print("MATH DETAILS KEYS:", list(res["math_details"].keys()))

if __name__ == "__main__":
    asyncio.run(run())
