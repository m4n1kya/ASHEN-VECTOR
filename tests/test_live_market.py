import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ashen_vector.api.services.live_market import LiveMarketService, LiveAnalysisRequest

@pytest.fixture
def service():
    return LiveMarketService()

@pytest.fixture
def df(service):
    return service.fetch_data("AAPL")

def test_01_fetch_returns_dataframe(service):
    df = service.fetch_data("TEST")
    assert isinstance(df, pd.DataFrame)

def test_02_fetch_has_expected_columns(df):
    expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    assert all(col in df.columns for col in expected_cols)

def test_03_fetch_has_1260_trading_days(df):
    assert len(df) == 1260

def test_04_fetch_index_is_datetime(df):
    assert isinstance(df.index, pd.DatetimeIndex)

def test_05_fetch_index_is_timezone_naive(df):
    assert df.index.tz is None

def test_06_high_is_greater_than_low(df):
    assert (df['High'] >= df['Low']).all()

def test_07_close_is_positive(df):
    assert (df['Close'] > 0).all()

def test_08_volume_is_positive(df):
    assert (df['Volume'] >= 0).all()

def test_09_deterministic_generation(service):
    df1 = service.fetch_data("MSFT")
    df2 = service.fetch_data("MSFT")
    pd.testing.assert_frame_equal(df1, df2)

def test_10_different_symbols_different_data(service):
    df1 = service.fetch_data("AAPL")
    df2 = service.fetch_data("TSLA")
    assert not df1['Close'].equals(df2['Close'])

def test_11_risk_calculation_volatility(service, df):
    risk = service.calculate_risk(df)
    assert 'volatility' in risk
    assert isinstance(risk['volatility'], float)

def test_12_risk_calculation_drawdown(service, df):
    risk = service.calculate_risk(df)
    assert 'max_drawdown' in risk
    assert risk['max_drawdown'] <= 0

def test_13_risk_calculation_rating(service, df):
    risk = service.calculate_risk(df)
    assert risk['rating'] in ["LOW", "MEDIUM", "HIGH"]

def test_14_risk_calculation_insufficient_data(service):
    short_df = pd.DataFrame({'Close': [100, 101, 102]})
    risk = service.calculate_risk(short_df)
    assert risk['rating'] == "UNKNOWN"
    assert risk['volatility'] == 0

def test_15_risk_calculation_high_vol(service):
    # Create fake high vol data
    dates = pd.date_range(end=datetime.now(), periods=252)
    prices = np.exp(np.random.normal(0, 0.1, 252)).cumprod() * 100
    df = pd.DataFrame({'Close': prices}, index=dates)
    risk = service.calculate_risk(df)
    assert risk['rating'] in ["HIGH", "MEDIUM"] # Depending on exact path

def test_16_analyze_returns_dict(service):
    req = LiveAnalysisRequest(symbol="TEST", models=["ALL"])
    res = service.analyze(req)
    assert isinstance(res, dict)

def test_17_analyze_includes_symbol(service):
    req = LiveAnalysisRequest(symbol="NVDA", models=["ALL"])
    res = service.analyze(req)
    assert res["symbol"] == "NVDA"

def test_18_analyze_includes_latest_price(service):
    req = LiveAnalysisRequest(symbol="META", models=["ALL"])
    res = service.analyze(req)
    assert res["latest_price"] > 0

def test_19_analyze_includes_reliability(service):
    req = LiveAnalysisRequest(symbol="AMZN", models=["ALL"])
    res = service.analyze(req)
    assert "reliability_score" in res

def test_20_analyze_includes_consensus(service):
    req = LiveAnalysisRequest(symbol="GOOGL", models=["ALL"])
    res = service.analyze(req)
    assert "consensus" in res
    assert isinstance(res["consensus"], dict)

def test_21_analyze_handles_unknown_symbol_name(service):
    req = LiveAnalysisRequest(symbol="XXX_INVALID", models=["ALL"])
    res = service.analyze(req)
    # the synthetic generator handles everything, name might be Unknown Company due to yf.Ticker
    assert "name" in res
