"""
Script to load example data and execute optimisation model
"""
from pathlib import Path

from chronos.lite import BatteryConfig, MarketData, BatteryModel

DATA_DIR = Path(__file__).parent / "data"


def main():
    battery_config = BatteryConfig(DATA_DIR / "battery_parameters.csv")
    market_data = MarketData(
        half_hourly_csv=DATA_DIR / "half-hourly-market.csv",
        hourly_csv=DATA_DIR / "hourly-market.csv",
    )
    model = BatteryModel(battery_config, market_data)
    model.optimise()
    print(model.solution)

if __name__ == "__main__":
    main()
