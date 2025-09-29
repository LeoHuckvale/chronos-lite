from typing import Iterable

import linopy
import pandas as pd
import xarray as xr

from chronos.lite.plot import plot_solution

#: Assumed minimum duration of a timestep in hours
TIMESTEP_DURATION = 0.5

#: Assume initial stored energy in the battery is 0.0 MWh
INITIAL_STORED_ENERGY = 0.0

#: Default solver is HiGHs, see https://pypi.org/project/highspy/
DEFAULT_SOLVER = "highs"


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
        self.market_data = market_data

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

        self._init_objective()


    def _init_variables(self):
        self.add_variables(binary=True, coords=[self.time], name="is charging")
        self.add_variables(binary=True, coords=[self.time], name="is discharging")
        self.add_variables(lower=0, upper=self.battery_config["Max charging rate"], coords=[self.time],
                           name="charge rate 30")
        self.add_variables(lower=0, upper=self.battery_config["Max discharging rate"], coords=[self.time],
                           name="discharge rate 30")
        self.add_variables(lower=0, upper=self.battery_config["Max charging rate"], coords=[self.time],
                           name="charge rate 60")
        self.add_variables(lower=0, upper=self.battery_config["Max discharging rate"], coords=[self.time],
                           name="discharge rate 60")

    def _init_constraints(self):
        # Charging cannot occur at the same time as discharging
        self.add_constraints(
            self.variables["is charging"] + self.variables["is discharging"] <= 1,
            name="charge/discharge exclusive"
        )

        # Combined charging rate across both markets cannot exceed max charging rate
        # Also charging cannot occur at the same time as discharging, due to "is charging" decision variable
        self.add_constraints(
            self.variables["charge rate 30"] + self.variables["charge rate 60"]
            <= self.variables["is charging"] * self.battery_config["Max charging rate"],
            name="max charge rate"
        )

        # Combined discharging rate across both markets cannot exceed max discharging rate
        # Also charging cannot occur at the same time as discharging, due to "is discharging" decision variable
        self.add_constraints(
            self.variables["discharge rate 30"] + self.variables["discharge rate 60"]
            <= self.variables["is discharging"] * self.battery_config["Max discharging rate"],
            name="max discharge rate"
        )

        # Cannot discharge more in a given timestep than the remaining available stored energy
        self.add_constraints(
            TIMESTEP_DURATION * (self.variables["discharge rate 30"] + self.variables["discharge rate 60"])
            <= self.stored_energy,
            name="available stored energy"
        )

        # Cannot charge more in a given timestep than the remaining available storage capacity
        self.add_constraints(
            TIMESTEP_DURATION * (self.variables["charge rate 30"] + self.variables["charge rate 60"])
            <= self.battery_config["Max storage volume"] - self.stored_energy,
            name="available storage capacity"
        )

        # Charging/discharging with hourly market commits to the full hour
        # TODO this is broken if the first half-hourly datapoint isn't aligned to the first half-hour, e.g. 00:00
        self.add_constraints(
            lhs=self.variables["charge rate 60"][::2],
            sign="=",
            rhs=self.variables["charge rate 60"][1::2],
            name="60 min charge full hour"
        )
        self.add_constraints(
            lhs=self.variables["discharge rate 60"][::2],
            sign="=",
            rhs=self.variables["discharge rate 60"][1::2],
            name="60 min discharge full hour"
        )

    def _init_objective(self):
        self.add_objective(
            (
                self.market_data["Price 30 min (£/MWh)"] * (
                    self.variables["discharge rate 30"] * self.battery_config["Battery discharging efficiency"]
                    - self.variables["charge rate 30"] / self.battery_config["Battery charging efficiency"]
                ) +
                self.market_data["Price 60 min (£/MWh)"] * (
                    self.variables["discharge rate 60"] * self.battery_config["Battery discharging efficiency"]
                    - self.variables["charge rate 60"] / self.battery_config["Battery charging efficiency"]
                )
            ),
            sense="max",
        )

    def optimise(self):
        """
        Solve the model.

        This method calls the `linopy.Model.solve` method, imposing our default solver choice.
        """
        super().solve(solver_name=DEFAULT_SOLVER)

    def plot_solution(self):
        """
        Plot the solution of the model.
        """
        if self.solution is None:
            raise RuntimeError("Optimisation hasn't been run. Need to run .solve() method.")
        plot_solution(self.battery_config, self.market_data, self.stored_energy, self.solution)
