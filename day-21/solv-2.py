#!/usr/bin/env python3.12

from collections import defaultdict
from functools import cache
from typing import List, Set, Tuple


INPUT_FILE_NAME: str = "test-input"
STEPS: int = 50
INPUT_FILE_NAME: str = "input"
STEPS: int = 26501365

GARDEN: str = "."
ROCK: str = "#"
START: str = "S"

LEFT: complex = complex(-1, 0)
RIGHT: complex = complex(1, 0)
UP: complex = complex(0, -1)
DOWN: complex = complex(0, 1)
DIRECTIONS: List[complex] = [LEFT, RIGHT, UP, DOWN]

with open(INPUT_FILE_NAME, "r") as input_file:
    grid = tuple(line.strip() for line in input_file)

for y, line in enumerate(grid):
    index_pos = line.find(START)
    if index_pos != -1:
        start_pos = complex(index_pos, y)


@cache
def get_cell(grid: Tuple[str], pos: complex) -> str:
    x = int(pos.real)
    y = int(pos.imag)
    width = len(grid[0])
    height = len(grid)
    while x < 0:
        x += width
    while x >= width:
        x = x % width
    while y < 0:
        y += height
    while y >= height:
        y = y % height
    return grid[y][x]


@cache
def get_next_positions(grid: Tuple[str], pos: complex) -> Set[complex]:
    global DIRECTIONS
    new_positions = set()
    for direction in DIRECTIONS:
        new_pos = pos + direction
        if get_cell(grid, new_pos) == ROCK:
            continue
        new_positions.add(new_pos)

    return new_positions


width = len(grid[0])
height = len(grid)
remainder = STEPS % height
repetitions = STEPS // height
grid_repetitions = 5

positions = (start_pos,)
for step in range(height * (grid_repetitions // 2) + remainder):
    new_positions = set()
    for pos in positions:
        new_positions.update(get_next_positions(grid, pos))

    positions = tuple(new_positions)
    # print(f"{step=} => {len(positions)=}")
    print(".", flush=True, end=(f" {step}\n" if step % 50 == 49 else ""))
print()

print(len(positions))

freq = defaultdict(int)
for pos in positions:
    freq[complex(pos.real // width, pos.imag // height)] += 1


print(f"{'':4} ", end="")
for gx in range(-(grid_repetitions // 2), grid_repetitions // 2 + 1):
    print(f"{gx:4} ", end="")
print()
for gy in range(-(grid_repetitions // 2), grid_repetitions // 2 + 1):
    print(f"{gy:4} ", end="")
    for gx in range(-(grid_repetitions // 2), grid_repetitions // 2 + 1):
        gpos = complex(gx, gy)
        v = freq[gpos]
        print(f"{v:4} ", end="")
    print("")

#        -2   -1    0    1    2
#   -2    0  943 5678  948    0
#   -1  943 6611 7457 6587  948
#    0 5678 7457 7520 7457 5674
#    1  950 6587 7457 6607  965
#    2    0  950 5674  965    0

solution = 0
solution += freq[complex(-2, -1)] * repetitions
solution += freq[complex(-2, 0)]
solution += freq[complex(-2, 1)] * repetitions

solution += freq[complex(-1, -1)] * (repetitions - 1)
solution += freq[complex(-1, 0)] * (repetitions * repetitions)
solution += freq[complex(-1, 1)] * (repetitions - 1)

solution += freq[complex(0, -2)]
solution += freq[complex(0, 0)] * ((repetitions - 1) * (repetitions - 1))
solution += freq[complex(0, 2)]

solution += freq[complex(1, -2)] * repetitions
solution += freq[complex(1, -1)] * (repetitions - 1)
solution += freq[complex(1, 1)] * (repetitions - 1)
solution += freq[complex(1, 2)] * repetitions

solution += freq[complex(2, 0)]

print(f"{solution=}")
