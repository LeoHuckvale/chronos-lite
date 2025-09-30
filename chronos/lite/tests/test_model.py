from pathlib import Path

import linopy
import pandas as pd
import pytest
import xarray as xr

from chronos.lite.data import load_battery_config, load_market_data
from chronos.lite.model import Model

TEST_DATA_DIR = Path(__file__).parent / "test_files"

@pytest.fixture
def battery_config():
    return load_battery_config(TEST_DATA_DIR / "test_battery_config.csv")

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

    def test_model_stored_energy(self, model):
        assert model.stored_energy.type == "LinearExpression"
