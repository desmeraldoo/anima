import random


def shuffle(targets: list[str]) -> str:
    if targets is None or targets == [""]:
        return ""
    s = []
    alt = [_ for _ in targets]
    # The shuffle is only valid if none of the destinations are the same as the starting points.
    while any([x == y for x, y in zip(targets, alt)]):
        random.shuffle(alt)
    for x, y in zip(targets, alt):
        s.append(f"{x} -> {y}")
    return "\n".join(s)
