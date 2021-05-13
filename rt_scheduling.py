import pandas as pd
import plotly.graph_objects as go
import sys

from collections import namedtuple
from plotly.graph_objs import Figure
from sweep_line import sweep_line
from typing import Tuple, Iterable


def main(argv):
    filename = str(argv[0])

    df = pd.read_csv(filename, sep=",", header=1,
                     names=[
                         "Compound", "Formula", "mOverZ", "z", "tStart",
                         "tStop",
                         "CollisionEnergy",
                         "Polarity"]
                     )

    def find_maximum(_: float, keys: set, accumulated_result: any):
        return max(accumulated_result, len(keys))

    OverlappingWindowsResult = namedtuple('OverlappingWindowsResult', 'last_count max_count current_window_start max_windows')

    def find_maximum_overlap(position: float, keys: set, accumulated_result: any) -> any:
        current_count = len(keys)

        is_rising = current_count > accumulated_result.last_count
        is_falling = current_count < accumulated_result.last_count
        was_max = accumulated_result.max_count == accumulated_result.last_count
        is_new_max = current_count > accumulated_result.max_count

        current_max = max(current_count, accumulated_result.max_count)
        max_windows = accumulated_result.max_windows
        current_window_start = accumulated_result.current_window_start
        if is_rising:
            if is_new_max:
                max_windows = []

            current_window_start = position

        if was_max and is_falling:
            max_windows.append((current_window_start, position))
            current_window_start = None

        return OverlappingWindowsResult(current_count, current_max, current_window_start, max_windows)

    def unique_key(index, row) -> str:
        return str(index) + str(row["mOverZ"])

    def event_points(data_frame: pd.DataFrame):
        for index, row in data_frame.iterrows():
            k = unique_key(index, row)
            yield row["tStart"], k
            yield row["tStop"], k

    # result = sweep_line(event_points(df), find_maximum, 0)
    # print(result)

    empty_result = OverlappingWindowsResult(0, 0, None, set())
    result = sweep_line(event_points(df), find_maximum_overlap, empty_result)

    print("Found maximum of", result.max_count, "overlapping windows:")
    for start, end in result.max_windows:
        print("From", start, "to", end)

    fig = create_window_plot(df, "tStart", "tStop", "mOverZ")
    fig = add_window_highlight(fig, result.max_windows)
    fig.show()


def create_window_plot(df: pd.DataFrame, start_col: str, stop_col: str, y_col: str):
    fig = go.Figure()
    axis_layout = dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ))
    fig.update_layout(
        title="Retention time window overlaps",
        plot_bgcolor="white",
        yaxis_title=y_col,
        xaxis_title="time (min)",
        xaxis=axis_layout,
        yaxis=axis_layout,
    )

    for i in df.index:
        x_values = [df.loc[i, start_col], df.loc[i, stop_col]]
        y_values = [df.loc[i, y_col], df.loc[i, y_col]]
        fig.add_trace(go.Scatter(x=x_values, y=y_values, mode="lines+markers", name=str(i)))

    return fig


def add_window_highlight(fig: Figure, max_windows: Iterable[Tuple[float, float]]) -> Figure:
    highlights = []
    for start, end in max_windows:
        highlights.append({
            'type': 'rect',
            'xref': 'x',
            'yref': 'paper',
            'x0': start,
            'y0': 0,
            'x1': end,
            'y1': 1000,
            'fillcolor': '#d3d3d3',
            'opacity': 0.2,
            'line': {
                'width': 0,
            }
        })
    fig.update_layout(shapes=highlights)
    return fig


if __name__ == '__main__':
    main(sys.argv[1:])