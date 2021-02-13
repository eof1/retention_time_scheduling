from typing import Iterable, Tuple


def sweep_line(event_points: Iterable[Tuple[float, str]], handle_event):
    current_keys = set()
    accumulated_result = handle_event(current_keys, 0)
    for _, key in sorted(event_points):
        if key in current_keys:
            current_keys.remove(key)
        else:
            current_keys.add(key)

        accumulated_result = handle_event(current_keys, accumulated_result)

    return accumulated_result
