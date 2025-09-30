import pandas as pd
from matplotlib import pyplot as plt


def plot_solution(
    battery_config: dict,
    market_data: pd.DataFrame,
    stored_energy,
    solution,
) -> plt.Figure:
    fig, (axis_price, axis_energy, axis_flow_30, axis_flow_60) = plt.subplots(4, figsize=(12, 6), sharex=True)
    axis_energy.set_ylim(0, 1.1*battery_config["Max storage volume"])
    axis_flow_30.set_ylim(-1.25*battery_config["Max discharging rate"], 1.25*battery_config["Max charging rate"])
    axis_price.set_ylabel("£")
    axis_energy.set_ylabel("E")
    axis_flow_30.set_ylabel("$r_{30}$")
    axis_flow_60.set_ylabel("$r_{60}$")
    axis_price.step(market_data.index, market_data["Price 30 min (£/MWh)"], color="orange", label="30min", where="post")
    axis_price.step(market_data.index, market_data["Price 60 min (£/MWh)"], color="purple", label="60min", where="post")
    axis_price.legend()
    axis_energy.fill_between(
        market_data.index,
        stored_energy.solution.values,
        color="blue",
    )
    axis_flow_30.fill_between(
        market_data.index,
        solution.variables["charge rate 30"],
        step="post",
        color="green",
        label="charging",
    )
    axis_flow_30.fill_between(
        market_data.index,
        -solution.variables["discharge rate 30"],
        step="post",
        color="red",
        label="discharging",
    )
    axis_flow_30.legend()
    axis_flow_60.fill_between(
        market_data.index,
        solution.variables["charge rate 60"],
        step="post",
        color="green",
        label="charging",
    )
    axis_flow_60.fill_between(
        market_data.index,
        -solution.variables["discharge rate 60"],
        step="post",
        color="red",
        label="discharging",
    )
    axis_flow_60.legend()

    return fig
