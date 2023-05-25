import random
from dataclasses import dataclass

import numpy as np
from tabulate import tabulate


@dataclass
class Result:
    name: str
    average: int
    std: float


def d10() -> int:
    return random.randint(1, 10)


def method_1() -> list[int]:
    results: list[int] = []
    while len(results) < 8:
        roll = d10()
        if roll > 3:
            results.append(roll)
    results = sorted(results)
    results[0] = 9
    return results


def method_2() -> list[int]:
    return [max(d10(), d10()) for _ in range(8)]


def method_3() -> list[int]:
    return [d10() for _ in range(8)]


def method_4() -> list[int]:
    return [d10() for _ in range(7)]


def main() -> None:
    results = []
    for method in [method_1, method_2, method_3, method_4]:
        samples = [method() for _ in range(10000)]
        average_stats = [sum(samp) / 8 for samp in samples]
        results.append(
            Result(
                name=method.__name__,
                average=np.average(average_stats),
                std=np.std(samples),
            )
        )
    print(tabulate(results, headers=["average", "std"], tablefmt="fancy_grid"))  # type: ignore[arg-type] # justification: mypy is being too strict


if __name__ == "__main__":
    main()
