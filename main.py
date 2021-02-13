import sys
from sweep_line import sweep_line
import pandas as pd


def main(argv):
    filename = str(argv[0])

    df = pd.read_csv(filename, sep=",", header=1,
                     names=[
                         "Compound", "Formula", "mOverZ", "z", "tStart",
                         "tStop",
                         "CollisionEnergy",
                         "Polarity"]
                     )

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


if __name__ == '__main__':
    main(sys.argv[1:])
