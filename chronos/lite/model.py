from typing import Iterable

import linopy
import pandas as pd
import xarray as xr

#: Assumed minimum duration of a timestep in hours
TIMESTEP_DURATION = 0.5

#: Assume initial stored energy in the battery is 0.0 MWh
INITIAL_STORED_ENERGY = 0.0

class Formulae:
    @staticmethod
    def stored_energy(
        initial_stored_energy: float,
        timestep_duration: float,
        charge_rate_30: xr.DataArray,
        charge_rate_60: xr.DataArray,
        charge_efficiency: float,
        discharge_rate_30: xr.DataArray,
        discharge_rate_60: xr.DataArray,
    ) -> Iterable[float]:
        return (
            initial_stored_energy +
            timestep_duration * (
                (charge_rate_30 + charge_rate_60) * charge_efficiency
                -
                (discharge_rate_30 + discharge_rate_60)
            ).shift(time=1).cumsum()
        )

class Model(linopy.Model):
    def __init__(self, battery_config: pd.Series, market_data: pd.DataFrame):
        super().__init__(force_dim_names=True)

        self.time = pd.Index(market_data.index, name="time")
        self.battery_config = battery_config

        self._init_variables()
        self.stored_energy = Formulae.stored_energy(
            INITIAL_STORED_ENERGY,
            TIMESTEP_DURATION,
            charge_rate_30=self.variables["charge rate 30"],
            charge_rate_60=self.variables["charge rate 60"],
            charge_efficiency=self.battery_config["Battery charging efficiency"],
            discharge_rate_30=self.variables["discharge rate 30"],
            discharge_rate_60=self.variables["discharge rate 60"],

        )

        self._init_constraints()

    def _init_variables(self):
        self.add_variables(binary=True, coords=[self.time], name="is charging")
        self.add_variables(binary=True, coords=[self.time], name="is discharging")
        self.add_variables(lower=0, upper=self.battery_config["Max charging rate"], coords=[self.time], name="charge rate 30")
        self.add_variables(lower=0, upper=self.battery_config["Max discharging rate"], coords=[self.time], name="discharge rate 30")
        self.add_variables(lower=0, upper=self.battery_config["Max charging rate"], coords=[self.time], name="charge rate 60")
        self.add_variables(lower=0, upper=self.battery_config["Max discharging rate"], coords=[self.time], name="discharge rate 60")

    def _init_constraints(self):
        ...
