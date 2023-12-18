#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


@dataclass
class C:
    x: int
    y: int

    def __hash__(self) -> int:
        return self.x + 10000 * self.y

    def __add__(self, other: C) -> C:
        return C(self.x + other.x, self.y + other.y)


@dataclass
class Instruction:
    direction: C
    steps: int
    color: str

    @staticmethod
    def direction_from_letter(letter: str) -> C:
        if letter == "R":
            return C(1, 0)
        if letter == "D":
            return C(0, 1)
        if letter == "L":
            return C(-1, 0)
        if letter == "U":
            return C(0, -1)

    @classmethod
    def from_line(cls, line: str) -> Instruction:
        parts = line.split()
        return Instruction(
            Instruction.direction_from_letter(parts[0]),
            int(parts[1]),
            parts[2].strip("(").strip(")").strip("#"),
        )


def get_edge(instructions: List[Instruction]) -> Tuple[Dict[C, int], C, C]:
    pos = C(0, 0)
    min_pos = C(0, 0)
    max_pos = C(0, 0)

    grid = defaultdict(int)
    grid[pos] = 1
    for instr in instructions:
        for _ in range(instr.steps):
            pos = pos + instr.direction
            grid[pos] = 1
            if pos.x < min_pos.x:
                min_pos = C(pos.x, min_pos.y)
            if pos.y < min_pos.y:
                min_pos = C(min_pos.x, pos.y)
            if pos.x > max_pos.x:
                max_pos = C(pos.x, max_pos.y)
            if pos.y > max_pos.y:
                max_pos = C(max_pos.x, pos.y)
    return (grid, min_pos, max_pos)


def find_an_inside_point(grid: Dict[C, int], min_pos: C, max_pos: C) -> C:
    for x in range(min_pos.x, max_pos.x + 1):
        maybe_result = C(x, min_pos.y + 1)
        if grid[C(x, min_pos.y)] == 1 and grid[maybe_result] == 0:
            return maybe_result
    raise Exception("oh uh")


def print_grid(grid: Dict[C, int], min_pos: C, max_pos: C) -> None:
    for y in range(min_pos.y, max_pos.y + 1):
        for x in range(min_pos.x, max_pos.x + 1):
            c = "#" if grid[C(x, y)] else "."
            print(c, end="")
        print()


def print_count(grid: Dict[C, int], min_pos: C, max_pos: C) -> None:
    count = sum(
        grid[C(x, y)]
        for x in range(min_pos.x, max_pos.x + 1)
        for y in range(min_pos.y, max_pos.y + 1)
    )
    print(f"{count=}")


def fill_grid(grid: Dict[C, int], fill_start_pos: C) -> None:
    to_visit = {fill_start_pos}
    while to_visit:
        pos = to_visit.pop()
        grid[pos] = 1
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                maybe_new_pos = C(pos.x + dx, pos.y + dy)
                if grid[maybe_new_pos] == 0:
                    to_visit.add(maybe_new_pos)


with open(INPUT_FILE_NAME, "r") as input_file:
    instructions = [Instruction.from_line(line.strip()) for line in input_file]

grid, min_pos, max_pos = get_edge(instructions)
print_grid(grid, min_pos, max_pos)
print_count(grid, min_pos, max_pos)
fill_start_pos = find_an_inside_point(grid, min_pos, max_pos)
print(f"{fill_start_pos=}")
fill_grid(grid, fill_start_pos)
print_grid(grid, min_pos, max_pos)
print_count(grid, min_pos, max_pos)
