"""Test data module."""

from pathlib import Path

import pandas as pd

from chronos.lite.data import load_battery_config, load_market_data

TEST_DATA_DIR = Path(__file__).parent / "test_files"


def test_load_battery_config():
    """Battery configuration data loads correctly."""
    actual_battery_config = load_battery_config(TEST_DATA_DIR / "test_battery_config.csv")
    expected_battery_config = {
        "Max charging rate": 1.0,
        "Max discharging rate": 2.0,
        "Max storage volume": 3.0,
        "Battery charging loss": 0.04,
        "Battery discharging loss": 0.05,
        "Lifetime (1)": 6.0,
        "Lifetime (2)": 7000,
        "Storage volume degradation rate": 0.008,
        "Capex": 900000.0,
        "Fixed Operational Costs": 10000.0,
    }
    assert actual_battery_config == expected_battery_config


def test_load_market_data():
    """Market data loads correctly."""
    actual_df = load_market_data(
        half_hourly_csv=TEST_DATA_DIR / "test_30min_market_data.csv",
        hourly_csv=TEST_DATA_DIR / "test_60min_market_data.csv",
    )

    expected_df = pd.DataFrame(
        data={
            "Price 30 min (£/MWh)": [
                48.47,
                49.81,
                53.65,
                52.48,
                47.25,
                47.18,
            ],
            "Price 60 min (£/MWh)": [
                51.89,
                51.89,
                55.49,
                55.49,
                51.06,
                51.06,
            ]
        },
        index=pd.Index(pd.date_range("2018-01-01", periods=6, freq="30min"), name="time")
    )
    pd.testing.assert_frame_equal(actual_df, expected_df, check_freq=False)
