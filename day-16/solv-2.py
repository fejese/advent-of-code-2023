#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


def dprint(message: str) -> None:
    # print(message)
    pass


@dataclass
class C:
    x: int
    y: int

    def __hash__(self) -> int:
        return f"{self.x}:{self.y}".__hash__()


@dataclass
class Beam:
    pos: C
    direction: C

    def step(self) -> Beam:
        return Beam(
            C(
                self.pos.x + self.direction.x,
                self.pos.y + self.direction.y,
            ),
            self.direction,
        )

    def is_valid(self, grid: List[str]) -> bool:
        if not (0 <= self.pos.x < len(grid[0])):
            return False
        if not (0 <= self.pos.y < len(grid)):
            return False

        return True


def solve(grid: List[str], start_beam: Beam) -> int:
    beams = [start_beam]
    visited = defaultdict(set)
    while beams:
        beam = beams.pop()
        dprint(f"Processing beam: {beam}")
        if beam.pos in visited and beam.direction in visited[beam.pos]:
            dprint(f"  visited already")
            continue

        visited[beam.pos].add(beam.direction)

        new_beams = []
        field = grid[beam.pos.y][beam.pos.x]
        if field == ".":
            new_beams.append(beam.step())
        elif field == "-":
            if beam.direction.y == 0:
                new_beams.append(beam.step())
            else:
                new_beams.append(Beam(C(beam.pos.x - 1, beam.pos.y), C(-1, 0)))
                new_beams.append(Beam(C(beam.pos.x + 1, beam.pos.y), C(1, 0)))
        elif field == "|":
            if beam.direction.x == 0:
                new_beams.append(beam.step())
            else:
                new_beams.append(Beam(C(beam.pos.x, beam.pos.y - 1), C(0, -1)))
                new_beams.append(Beam(C(beam.pos.x, beam.pos.y + 1), C(0, 1)))
        elif field == "/":
            if beam.direction == C(1, 0):
                new_beams.append(Beam(C(beam.pos.x, beam.pos.y - 1), C(0, -1)))
            elif beam.direction == C(-1, 0):
                new_beams.append(Beam(C(beam.pos.x, beam.pos.y + 1), C(0, 1)))
            if beam.direction == C(0, 1):
                new_beams.append(Beam(C(beam.pos.x - 1, beam.pos.y), C(-1, 0)))
            elif beam.direction == C(0, -1):
                new_beams.append(Beam(C(beam.pos.x + 1, beam.pos.y), C(1, 0)))
        elif field == "\\":
            if beam.direction == C(1, 0):
                new_beams.append(Beam(C(beam.pos.x, beam.pos.y + 1), C(0, 1)))
            elif beam.direction == C(-1, 0):
                new_beams.append(Beam(C(beam.pos.x, beam.pos.y - 1), C(0, -1)))
            if beam.direction == C(0, 1):
                new_beams.append(Beam(C(beam.pos.x + 1, beam.pos.y), C(1, 0)))
            elif beam.direction == C(0, -1):
                new_beams.append(Beam(C(beam.pos.x - 1, beam.pos.y), C(-1, 0)))

        for beam in new_beams:
            if beam.is_valid(grid):
                dprint(f"  new beam: {beam} (valid)")
                beams.append(beam)
            else:
                dprint(f"  new beam: {beam} (invalid)")

    powered = len(visited)
    print(f"{start_beam=} => {powered}")

    return powered


def get_starting_beams(grid: List[str]) -> List[Beam]:
    width = len(grid[0])
    height = len(grid)
    return [
        *[Beam(C(x, 0), C(0, 1)) for x in range(width)],
        *[Beam(C(0, y), C(1, 0)) for y in range(height)],
        *[Beam(C(x, height - 1), C(0, -1)) for x in range(width)],
        *[Beam(C(width - 1, y), C(-1, 0)) for y in range(height)],
    ]


with open(INPUT_FILE_NAME, "r") as input_file:
    grid = [line.strip() for line in input_file]


solution = max(solve(grid, starting_beam) for starting_beam in get_starting_beams(grid))
print(f"{solution=}")
