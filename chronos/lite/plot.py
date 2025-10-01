"""Utility functions to plot data."""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_solution(
    solution_df: pd.DataFrame,
) -> go.Figure:
    """Generate a Plotly figure showing key data from battery optimisation solution.

    Includes four axes:
    - Market prices (half-hourly and hourly)
    - Stored energy in the battery
    - Charge/discharge flow with the half-hourly market
    - Charge/discharge flow with the hourly market
    """

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.01)
    fig.add_trace(
        go.Scatter(x=solution_df.index, y=solution_df["Price 30 min (£/MWh)"], marker_color="orange",
                   name="Price 30 min",
                   line_shape="hv"),
        row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(x=solution_df.index, y=solution_df["Price 60 min (£/MWh)"], marker=dict(color="purple"),
                   name="Price 60 min",
                   line_shape="hv"),
        row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(x=solution_df.index, y=solution_df["stored energy"], marker_color="blue", fill="tozeroy",
                   name="Stored Energy"),
        row=2, col=1,
    )
    fig.add_trace(
        go.Scatter(x=solution_df.index, y=solution_df["charge rate 30"], marker_color="green", fill="tozeroy",
                   name="Charge rate (30min)",
                   line_shape="hv"),
        row=3, col=1,
    )
    fig.add_trace(
        go.Scatter(x=solution_df.index, y=-solution_df["discharge rate 30"], marker_color="red", fill="tozeroy",
                   name="Discharge rate (30 min)", line_shape="hv"),
        row=3, col=1,
    )
    fig.add_trace(
        go.Scatter(x=solution_df.index, y=solution_df["charge rate 60"], marker_color="green", fill="tozeroy",
                   name="Charge rate (60min)",
                   line_shape="hv"),
        row=4, col=1,
    )
    fig.add_trace(
        go.Scatter(x=solution_df.index, y=-solution_df["discharge rate 60"], marker_color="red", fill="tozeroy",
                   name="Discharge rate (60 min)", line_shape="hv"),
        row=4, col=1,
    )
    fig.add_hline(y=0, row=3, col=1)
    fig.add_hline(y=0, row=4, col=1)
    fig.update_yaxes(title_text="Price (£/MWh)", row=1, col=1)
    fig.update_yaxes(title_text="Stored Energy<br>(MWh)", row=2, col=1)
    fig.update_yaxes(title_text="Charge/Discharge<br>Power<br>30min market<br>(MW)", row=3, col=1)
    fig.update_yaxes(title_text="Charge/Discharge<br>Power<br>60min market<br> (MW)", row=4, col=1)
    fig.update_layout(autosize=False, width=1200, height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()
    return fig
