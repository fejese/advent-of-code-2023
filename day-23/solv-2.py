#!/usr/bin/env python3.12

from collections import defaultdict
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


with open(INPUT_FILE_NAME, "r") as input_file:
    grid = tuple(line.strip() for line in input_file)

start_x: int = grid[0].find(PATH)
START: C = (start_x, 0)
goal_x: int = grid[-1].find(PATH)
GOAL: C = (goal_x, len(grid) - 1)

print(f"Start: {START}")
print(f"Goal: {GOAL}")

to_visit: Set[C] = {START}
possible_paths: Dict[C, Set[Tuple[C]]] = defaultdict(set)
possible_paths[START].add(tuple())

while to_visit:
    print(f"{len(to_visit)} positions left to explore")

    new_to_visit = set()
    for current in to_visit:
        next_positions = get_next_positions(grid, current)

        for path in possible_paths[current]:
            new_path = set(path)
            new_path.add(current)
            new_path = tuple(sorted(new_path))
            for next_pos in next_positions:
                if next_pos in path:
                    continue
                if new_path not in possible_paths[next_pos]:
                    possible_paths[next_pos].add(new_path)
                    new_to_visit.add(next_pos)
                else:
                    pass

    to_visit = new_to_visit

print(max(len(path) for path in possible_paths[GOAL]))
