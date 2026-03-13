import numpy as np
import pandas as pd
import pytest
import talib

from core.feature_engineering.technical_features import TechnicalFeatureEngine


def test_add_moving_averages():
    # Create sample data
    data = {"Close": np.random.random(100) * 100}
    df = pd.DataFrame(data)

    # Initialize engineer
    engineer = TechnicalFeatureEngine()

    # Run
    df_out = engineer._add_moving_averages(df.copy())

    # Verify results
    assert "sma_5" in df_out.columns
    assert "ema_5" in df_out.columns

    # Check expected calculation for sma 5
    expected_sma_5 = talib.SMA(df["Close"].values, timeperiod=5)
    np.testing.assert_array_almost_equal(df_out["sma_5"].values, expected_sma_5)


def test_add_volatility_indicators():
    # Create sample data
    data = {
        "High": np.random.random(100) * 110,
        "Low": np.random.random(100) * 90,
        "Close": np.random.random(100) * 100,
        "Open": np.random.random(100) * 100,
    }
    df = pd.DataFrame(data)

    # Initialize engineer
    engineer = TechnicalFeatureEngine()

    # Run
    df_out = engineer._add_volatility_indicators(df.copy())

    # Verify results
    assert "volatility_5" in df_out.columns

    # Check expected calculation for std 5
    expected_std_5 = talib.STDDEV(df["Close"].values, timeperiod=5, nbdev=1)
    np.testing.assert_array_almost_equal(df_out["volatility_5"].values, expected_std_5)


def test_add_volume_indicators():
    data = {
        "Close": np.random.random(100) * 100,
        "Volume": np.random.random(100) * 1000,
    }
    df = pd.DataFrame(data)

    # Initialize engineer
    engineer = TechnicalFeatureEngine()

    # Run
    df_out = engineer._add_volume_indicators(df.copy())

    # Verify results
    assert "volume_ma_5" in df_out.columns

    # Check expected calculation for volume sma
    expected_vol_sma_5 = talib.SMA(df["Volume"].values, timeperiod=5)
    np.testing.assert_array_almost_equal(
        df_out["volume_ma_5"].values, expected_vol_sma_5
    )
