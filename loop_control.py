import sys
import pandas as pd


def main(argv):
    filename = str(argv[0])

    load_csv(filename)


class EventPoint:
    position: float
    key: None

    def __init__(self, position, key):
        self.position = position
        self.key = key


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
    eventPoints = []
    for index, row in df.iterrows():
        eventPoints.append((row["tStart"], str(index)))
        eventPoints.append((row["tStop"], str(index)))

    return eventPoints


def load_csv(filename):
    df = pd.read_csv(filename, sep=",", header=1,
                     names=[
                         "Compound", "Formula", "mOverZ", "z", "tStart",
                         "tStop",
                         "CollisionEnergy",
                         "Polarity"]
                     )

    def handleEventPoint(keys):
        print(len(keys))

    sweep_line(lambda: eventPoints(df), lambda x: handleEventPoint(x))


if __name__ == '__main__':
    main(sys.argv[1:])
