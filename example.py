"""
Script to load example data and execute optimisation model
"""
from pathlib import Path

from chronos.lite.data import load_battery_config, load_market_data
from chronos.lite.model import Model

DATA_DIR = Path(__file__).parent / "data"


def main():
    battery_config = load_battery_config(DATA_DIR / "battery_parameters.csv")
    market_data = load_market_data(
        half_hourly_csv=DATA_DIR / "half-hourly-market.csv",
        hourly_csv=DATA_DIR / "hourly-market.csv",
    )
    model = Model(battery_config, market_data)
    model.optimise()
    print(model.solution)


if __name__ == "__main__":
    main()
