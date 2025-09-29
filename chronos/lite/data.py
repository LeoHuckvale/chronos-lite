"""
Battery and Market Data Utility Functions
=========================================

This module provides utility functions for loading battery configuration and market data files.

"""
import os
from typing import Optional

import pandas as pd


def load_battery_config(path: os.PathLike) -> dict:
    """
    Load battery config from CSV file

    path: Path to CSV file containing battery config.
    """
    return pd.read_csv(path, index_col=0)["Values"].to_dict()


def load_market_data(half_hourly_csv: os.PathLike, hourly_csv: os.PathLike, nrows: int | None = None) -> pd.DataFrame:
    """
    Load market data from CSV file

    half_hourly_csv: Path to CSV file containing half-hourly price data.
    hourly_csv: Path to CSV file containing hourly price data.
   
    CSV files should both be of the format:
        ```
        Datetime, Price (£/MWh)
        dd/mm/YYYY HH:MM, #.#
        ```

        e.g.

        ```
        Datetime, Price (£/MWh)
        18/09/2018 01:30, 52.3
        18/09/2018 02:00, 50.5
        18/09/2018 02:30, 49.2
        18/09/2018 03:00, 51.6
        ```
    """
    if nrows % 2 != 0:
        raise ValueError("nrows must be even")

    half_hourly_market_series = pd.read_csv(
        half_hourly_csv,
        index_col=0,
        skiprows=1,
        nrows=nrows,
        names=["Price 30 min (£/MWh)"],
    ).iloc[:, 0]
    half_hourly_market_series.index = pd.to_datetime(half_hourly_market_series.index, format="%d/%m/%Y %H:%M")
    hourly_market_series = pd.read_csv(
        hourly_csv,
        index_col=0,
        skiprows=1,
        nrows=nrows/2 if nrows is not None else None,
        names=["Price 60 min (£/MWh)"],
    ).iloc[:, 0]
    hourly_market_series.index = pd.to_datetime(hourly_market_series.index, format="%d/%m/%Y %H:%M")

    aligned_hourly_market_series = pd.concat([
        hourly_market_series,
        hourly_market_series.set_axis(hourly_market_series.index + pd.to_timedelta(30, unit='m')),
    ]).sort_index()

    index = half_hourly_market_series.index
    index.name = "Time"

    return pd.DataFrame({
        "Price 30 min (£/MWh)": half_hourly_market_series,
        "Price 60 min (£/MWh)": aligned_hourly_market_series,
    }, index=index)
