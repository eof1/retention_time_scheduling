import sys
from sweep_line import sweep_line
import pandas as pd
import plotly.graph_objects as go


def main(argv):
    filename = str(argv[0])

    df = pd.read_csv(filename, sep=",", header=1,
                     names=[
                         "Compound", "Formula", "mOverZ", "z", "tStart",
                         "tStop",
                         "CollisionEnergy",
                         "Polarity"]
                     )
    plotData(df)

    def handle_event_point(keys: set, accumulated_result: any):
        return max(accumulated_result, len(keys))

    def key(index, row) -> str:
        return str(index) + str(row["mOverZ"])

    def event_points(data_frame: pd.DataFrame):
        for index, row in data_frame.iterrows():
            k = key(index, row)
            yield row["tStart"], k
            yield row["tStop"], k

    result = sweep_line(event_points(df), handle_event_point)
    print(result)


def plotData(df: pd.DataFrame) -> None:
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
        plot_bgcolor="white",
        yaxis_title="m/z",
        xaxis_title="time (min)",
        xaxis=axis_layout,
        yaxis=axis_layout,
    )
    for index, row in df.iterrows():
        fig.add_trace(
            go.Scatter(x=[row["tStart"], row["tStop"]], y=[row["mOverZ"], row["mOverZ"]], mode="lines+markers", name=str(index)))

    fig.show()


def createAdder(y):
    def add(y: int):
        return lambda b: lambda a: a + y

    return add


if __name__ == '__main__':
    main(sys.argv[1:])
