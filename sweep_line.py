from typing import Iterable, Tuple, Hashable, Callable


def sweep_line(event_points: Iterable[Tuple[float, Hashable]], handle_event: Callable[[float, set, any], any], seed: any):
    current_items = set()
    accumulated_result = seed
    for position, item in sorted(event_points):
        if item in current_items:
            current_items.remove(item)
        else:
            current_items.add(item)

        accumulated_result = handle_event(position, current_items, accumulated_result)

    return accumulated_result


