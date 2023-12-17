#!/usr/bin/env python3.12

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from typing import Collection, Tuple


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


Grid = Tuple[str]


@dataclass
class C:
    x: int
    y: int

    def __hash__(self) -> int:
        return self.x + 1000 * self.y

    def reverse(self) -> C:
        return C(-self.x, -self.y)

    def __add__(self, other: C) -> C:
        return C(self.x + other.x, self.y + other.y)

    def is_valid_pos(self, grid: Grid) -> bool:
        return (0 <= self.x < len(grid[0])) and (0 <= self.y < len(grid))


@cache
def next_possible_directions(curr_dir: C) -> Collection[C]:
    return [
        d for d in [C(1, 0), C(-1, 0), C(0, 1), C(0, -1)] if d != curr_dir.reverse()
    ]


@cache
def next_directions(curr_dir: C, dir_steps: int) -> Collection[C]:
    return [
        d for d in next_possible_directions(curr_dir) if dir_steps < 3 or d != curr_dir
    ]


def solve(grid: Grid) -> int:
    start = C(0, 0)
    target = C(len(grid[0]) - 1, len(grid) - 1)

    costs = defaultdict(lambda: 99999999)

    costs[(start, C(1, 0), 0)] = 0
    costs[(start, C(0, 1), 0)] = 0
    to_visit = {(start, C(1, 0), 0), (start, C(0, 1), 0)}

    while to_visit:
        new_to_visit = set()
        for curr_key in to_visit:
            pos, curr_dir, dir_steps = curr_key
            cost = costs[curr_key]
            for next_dir in next_directions(curr_dir, dir_steps):
                next_pos = next_dir + pos
                if not next_pos.is_valid_pos(grid):
                    continue
                next_dir_steps = dir_steps + 1 if curr_dir == next_dir else 1
                next_cost = cost + int(grid[next_pos.y][next_pos.x])
                next_key = (next_pos, next_dir, next_dir_steps)
                if costs[next_key] > next_cost:
                    costs[next_key] = next_cost
                    new_to_visit.add(next_key)

        to_visit = new_to_visit

    return min(v for k, v in costs.items() if k[0] == target)


with open(INPUT_FILE_NAME, "r") as input_file:
    grid = tuple(line.strip() for line in input_file)
    print(solve(grid))
