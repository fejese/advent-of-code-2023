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

    def __mul__(self, m: int) -> C:
        if not isinstance(m, int):
            raise Exception()

        return C(self.x * m, self.y * m)


@dataclass
class Shape:
    points: List[C]
    edge_points: int

    def get_area(self) -> int:
        points = [*self.points, self.points[0]]
        # print(f"{points=}")

        area = 0
        for i in range(len(points) - 1):
            area += points[i].x * points[i + 1].y
            area -= points[i].y * points[i + 1].x

        return area // 2


@dataclass
class Instruction:
    direction: C
    steps: int

    @staticmethod
    def direction_from_letter(letter: str) -> C:
        dir_code = int(letter) if letter in "0123" else "RDLU".index(letter)
        return [C(1, 0), C(0, 1), C(-1, 0), C(0, -1)][dir_code]

    @classmethod
    def from_line(cls, line: str) -> Instruction:
        parts = line.split()

        color = parts[2].strip("(").strip(")").strip("#")
        return Instruction(
            Instruction.direction_from_letter(color[5]),
            int(color[:5], 16),
        )


def get_shape(instructions: List[Instruction]) -> Shape:
    pos = C(0, 0)
    points = []

    circ = 0
    for instr in instructions:
        pos = pos + instr.direction * instr.steps
        circ += instr.steps
        points.append(pos)

    return Shape(points, circ)


with open(INPUT_FILE_NAME, "r") as input_file:
    instructions = [Instruction.from_line(line.strip()) for line in input_file]

shape = get_shape(instructions)

A = shape.get_area()
B = shape.edge_points
print(f"{A=}")
print(f"{B=}")
I = A - B // 2 + 1
print(f"I = A - B/2 + 1 = {A} - {B}/2 + 1 = {I}")
print(f"{I + B = }")
