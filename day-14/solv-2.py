#!/usr/bin/env python3.12

from functools import cache
from typing import List, Tuple


# INPUT_FILE_NAME: str = "test-input"
CYCLES: int = 1000000000
INPUT_FILE_NAME: str = "input"


def print_grid(g: Tuple[Tuple[str]]) -> None:
    [print("".join(line)) for line in g]
    print()


def tilt(grid: List[Tuple[str]], direction: Tuple[int, int]) -> None:
    global W
    global H
    movement = True
    while movement:
        movement = False
        for x in range(W):
            for y in range(H):
                dst_x = x + direction[0]
                dst_y = y + direction[1]
                if dst_x < 0 or dst_y < 0 or dst_x >= W or dst_y >= H:
                    continue

                if (grid[dst_y][dst_x], grid[y][x]) == (EMPTY, ROUNDED):
                    movement = True
                    grid[dst_y][dst_x], grid[y][x] = (ROUNDED, EMPTY)


def cycle_grid(grid: List[Tuple[str]]) -> None:
    for direction in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        tilt(grid, direction)


def hash_grid(grid: List[Tuple[str]]) -> str:
    global W
    global H
    return ";".join(
        f"{x},{y}" for x in range(W) for y in range(H) if grid[y][x] == ROUNDED
    )


def score(grid: List[List[str]]) -> int:
    global W
    global H
    total_load = 0
    for x in range(W):
        for y in range(H):
            if grid[y][x] == ROUNDED:
                load = H - y
                total_load += load
    return total_load


with open(INPUT_FILE_NAME, "r") as input_file:
    grid = [list(line.strip()) for line in input_file]

W = len(grid[0])
H = len(grid)
ROUNDED = "O"
CUBE = "#"
EMPTY = "."

print_grid(grid)

cache = {}
cycle = 1
while cycle <= CYCLES:
    ghash = hash_grid(grid)
    if ghash in cache:
        prev = cache[ghash]
        # print(f"repeat: {cycle}, {prev=}")
        loop_length = cycle - prev
        while cycle + loop_length < CYCLES:
            cycle += loop_length
    cache[ghash] = cycle
    # print(f"After {cycle} cycles:")
    cycle_grid(grid)
    cycle += 1

total_load = score(grid)

print(f"{total_load=}")
