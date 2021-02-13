import sys
import pandas as pd


def main(argv):
    filename = str(argv[0])

    load_csv(filename)


def sweep_line(epFunc, eventFunc):
    event_points = []
    for position, key in epFunc():
        event_points.append((position, key))

    event_points.sort()

    current_keys = set()
    for _, key in event_points:
        if key in current_keys:
            current_keys.remove(key)
        else:
            current_keys.add(key)

        eventFunc(current_keys)


def eventPoints(df):
    for index, row in df.iterrows():
        yield row["tStart"], str(index) + str(row["mOverZ"])
        yield row["tStop"], str(index) + str(row["mOverZ"])


def load_csv(filename: str):
    df = pd.read_csv(filename, sep=",", header=1,
                     names=[
                         "Compound", "Formula", "mOverZ", "z", "tStart",
                         "tStop",
                         "CollisionEnergy",
                         "Polarity"]
                     )

    def handle_event_point(keys: set):
        print(len(keys));
        #return lambda x: max(x, len(keys))

    result = sweep_line(lambda: eventPoints(df), lambda x: handle_event_point(x))


if __name__ == '__main__':
    main(sys.argv[1:])
