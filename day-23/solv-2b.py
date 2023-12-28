#!/usr/bin/env python3.12

import cProfile

from collections import defaultdict
from datetime import datetime, timedelta
from functools import cache
from typing import Dict, List, Tuple, Set

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

C = Tuple[int, int]

PATH = "."
FOREST = "#"
DIRECTIONS: List[C] = [(0, 1), (0, -1), (-1, 0), (1, 0)]


@cache
def get_next_positions(grid: Tuple[str], position: C) -> Set[C]:
    positions = set()
    for direction in DIRECTIONS:
        next_pos = tuple(int(position[axis] + direction[axis]) for axis in range(2))
        if not (0 <= next_pos[0] < len(grid[0])):
            continue
        if not (0 <= next_pos[1] < len(grid)):
            continue
        next_tile = grid[next_pos[1]][next_pos[0]]
        if next_tile == FOREST:
            continue

        positions.add(next_pos)
    return positions


def insert_sorted(path: Tuple[C, ...], position: C) -> Tuple[C, ...]:
    return tuple(
        [
            *[p for p in path if p < position],
            position,
            *[p for p in path if p >= position],
        ]
    )


def get_new_path(path: Tuple[C, ...], position: C) -> Tuple[C, ...]:
    new_path = set(path)
    new_path.add(position)
    return tuple(sorted(new_path))


def main() -> None:
    # start = datetime.now()

    with open(INPUT_FILE_NAME, "r") as input_file:
        grid = tuple(line.strip() for line in input_file)

    start_x: int = grid[0].find(PATH)
    START: C = (start_x, 0)
    goal_x: int = grid[-1].find(PATH)
    GOAL: C = (goal_x, len(grid) - 1)

    print(f"Start: {START}")
    print(f"Goal: {GOAL}")

    to_visit: Dict[C, Set[Tuple[C, ...]]] = defaultdict(set)
    to_visit[START].add(tuple())
    possible_paths: Dict[C, Set[Tuple[C]]] = defaultdict(set)
    possible_path_lengths: Dict[C, int] = defaultdict(int)
    possible_paths[START].add(tuple())

    while to_visit:
        print(f"{len(to_visit)} positions left to explore")

        new_to_visit = defaultdict(set)
        for current, new_current_paths in to_visit.items():
            next_positions = get_next_positions(grid, current)

            for path in new_current_paths:
                # new_path = get_new_path(path, current)
                new_path = insert_sorted(path, current)
                new_path_length = len(new_path)
                for next_pos in next_positions:
                    if next_pos in path:
                        continue
                    if new_path_length < possible_path_lengths[next_pos]:
                        continue
                    if new_path in possible_paths[next_pos]:
                        continue

                    if new_path_length > possible_path_lengths[next_pos]:
                        possible_paths[next_pos] = {new_path}
                        possible_path_lengths[next_pos] = new_path_length
                    else:
                        possible_paths[next_pos].add(new_path)

                    new_to_visit[next_pos].add(new_path)

        to_visit = new_to_visit

        # now = datetime.now()
        # if now - start > timedelta(minutes=1):
        #     break

    if GOAL in possible_paths:
        print(max(len(path) for path in possible_paths[GOAL]))
    else:
        print("No solution found!")


cProfile.run("main()", sort="tottime")
print(get_next_positions.cache_info())
