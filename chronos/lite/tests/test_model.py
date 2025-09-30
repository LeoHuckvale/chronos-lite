from pathlib import Path

import linopy
import pandas as pd
import pytest

from chronos.lite.data import load_battery_config, load_market_data
from chronos.lite.model import Model

TEST_DATA_DIR = Path(__file__).parent / "test_files"

@pytest.fixture
def battery_config():
    return load_battery_config(TEST_DATA_DIR / "test_battery_config.csv")

@pytest.fixture
def realistic_battery_config():
    return load_battery_config(TEST_DATA_DIR / "realistic_battery_config.csv")

@pytest.fixture
def market_data():
    return load_market_data(
        half_hourly_csv=TEST_DATA_DIR / "test_30min_market_data.csv",
        hourly_csv=TEST_DATA_DIR / "test_60min_market_data.csv",
    )

@pytest.fixture
def model(battery_config, market_data):
    return Model(battery_config, market_data)


class TestModel:
    def test_model_init(self, model):
        pass

    def test_model_subclasses_linopy(self, model):
        assert isinstance(model, linopy.Model)

    def test_model_forces_dim_names(self, model):
        assert model._force_dim_names

    def test_model_coords(self, model):
        pd.testing.assert_index_equal(
            model.variables.coords.to_index(),
            pd.Index(pd.date_range("2018-01-01", periods=6, freq="30min"), name="time")
        )

    def test_model_variable_is_charging(self, model):
        # "is charging" decision variable is:
        # boolean
        assert (model.variables["is charging"].type == "Binary Variable")
        # lower bounded at 0
        assert (model.variables["is charging"].lower == 0.0).all()
        # upper bounded at 1
        assert (model.variables["is charging"].upper == 1.0).all()

    def test_model_variable_is_discharging(self, model):
        # "is discharging" decision variable is:
        # boolean
        assert (model.variables["is discharging"].type == "Binary Variable")
        # lower bounded at 0
        assert (model.variables["is discharging"].lower == 0.0).all()
        # upper bounded at 1
        assert (model.variables["is discharging"].upper == 1.0).all()

    def test_model_variable_charge_rate_30(self, model):
        # charge rate into 30min market is:
        # continuous
        assert (model.variables["charge rate 30"].type == "Continuous Variable")
        # lower bounded at 0
        assert (model.variables["charge rate 30"].lower == 0.0).all()
        # upper bounded at max charge rate
        assert (model.variables["charge rate 30"].upper == 1.0).all()

    def test_model_variable_discharge_rate_30(self, model):
        # discharge rate into 30min market is:
        # continuous
        assert (model.variables["discharge rate 30"].type == "Continuous Variable")
        # lower bounded at 0
        assert (model.variables["discharge rate 30"].lower == 0.0).all()
        # upper bounded at max discharge rate
        assert (model.variables["discharge rate 30"].upper == 2.0).all()

    def test_model_variable_charge_rate_60(self, model):
        # charge rate into 60min market is:
        # continuous
        assert (model.variables["charge rate 60"].type == "Continuous Variable")
        # lower bounded at 0
        assert (model.variables["charge rate 60"].lower == 0.0).all()
        # upper bounded at max charge rate
        assert (model.variables["charge rate 60"].upper == 1.0).all()

    def test_model_variable_discharge_rate_60(self, model):
        # discharge rate into 60min market is:
        # continuous
        assert (model.variables["discharge rate 60"].type == "Continuous Variable")
        # lower bounded at 0
        assert (model.variables["discharge rate 60"].lower == 0.0).all()
        # upper bounded at max discharge rate
        assert (model.variables["discharge rate 60"].upper == 2.0).all()

class TestBehaviour:
    def test_charge_discharge_30min(self, realistic_battery_config):
        time = pd.Index(pd.date_range("2018-01-01", periods=2, freq="30min"), name="time")
        market_data = pd.DataFrame(
            data={
                "Price 30 min (£/MWh)": [40.0, 50.0],
                "Price 60 min (£/MWh)": [45.0, 45.0],
            },
            index=time,
        )
        model = Model(realistic_battery_config, market_data)
        model.solve()
        pd.testing.assert_frame_equal(
            model.variables.solution.to_dataframe(),
            pd.DataFrame(
                data={
                    "is charging": [1.0, 0.0],
                    "is discharging": [0.0, 1.0],
                    "charge rate 30": [2.0, 0.0],  # first half-hour subject to charging losses, 0.95 MWh stored
                    "discharge rate 30": [0.0, 1.9],  # second half-hour discharges all of stored energy = 2x0.95=1.9MW
                    "charge rate 60": [0.0, 0.0],
                    "discharge rate 60": [0.0, 0.0],
                },
                index=time,
            )
        )

    def test_charge_discharge_60min(self, realistic_battery_config):
        time = pd.Index(pd.date_range("2018-01-01", periods=4, freq="30min"), name="time")
        market_data = pd.DataFrame(
            data={
                "Price 30 min (£/MWh)": [45.0, 50.0, 50.0, 50.0],
                "Price 60 min (£/MWh)": [40.0, 40.0, 55.0, 55.0],
            },
            index=time,
        )
        model = Model(realistic_battery_config, market_data)
        model.solve()
        pd.testing.assert_frame_equal(
            model.variables.solution.to_dataframe(),
            pd.DataFrame(
                data={
                    "is charging": [1.0, 1.0, 0.0, 0.0],
                    "is discharging": [0.0, 0.0, 1.0, 1.0],
                    "charge rate 30": [0.0, 0.0, 0.0, 0.0],
                    "discharge rate 30": [0.0, 0.0, 0.0, 0.0],
                    "charge rate 60": [2.0, 2.0, 0.0, 0.0],  # hour 1 subject to charging losses, 1.9MWh stored
                    "discharge rate 60": [0.0, 0.0, 1.9, 1.9],  # hour 2 discharges all of stored energy,
                },
                index=time,
            )
        )
