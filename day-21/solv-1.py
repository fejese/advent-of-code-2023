#!/usr/bin/env python3

from typing import List


# INPUT_FILE_NAME: str = "test-input"
# STEPS: int = 6
INPUT_FILE_NAME: str = "input"
STEPS: int = 64

GARDEN: str = "."
ROCK: str = "#"
START: str = "S"

LEFT: complex = complex(-1, 0)
RIGHT: complex = complex(1, 0)
UP: complex = complex(0, -1)
DOWN: complex = complex(0, 1)
DIRECTIONS: List[complex] = [LEFT, RIGHT, UP, DOWN]

with open(INPUT_FILE_NAME, "r") as input_file:
    grid = [line.strip() for line in input_file]

for y, line in enumerate(grid):
    index_pos = line.find(START)
    if index_pos != -1:
        start_pos = complex(index_pos, y)

positions = {start_pos}
for step in range(STEPS):
    new_positions = set()
    for pos in positions:
        for direction in DIRECTIONS:
            new_pos = pos + direction
            if grid[int(new_pos.imag)][int(new_pos.real)] == ROCK:
                continue
            new_positions.add(new_pos)
    positions = new_positions

print(len(positions))
