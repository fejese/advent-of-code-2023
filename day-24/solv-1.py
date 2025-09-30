#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

INPUT_FILE_NAME: str = "test-input"
C_RANGE: Tuple[int, int] = (7, 27)
INPUT_FILE_NAME: str = "input"
C_RANGE: Tuple[int, int] = (200000000000000, 400000000000000)


@dataclass
class Hail:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    def intersection(self, other: Hail) -> Optional[Tuple[float, float, float]]:
        if self.vy * other.vx == other.vy * self.vx:
            return None

        if self.x == other.x and self.y == other.y:
            return (self.x, other.x)

        py = ((self.x - other.x - self.y * self.vx / self.vy) * other.vy / other.vx + other.y) / (1 - self.vx * other.vy / self.vy / other.vx)
        px = (py - self.y) * self.vx / self.vy + self.x

        if (px - self.x) / self.vx < 0:
            return None
        if (px - other.x) / other.vx < 0:
            return None

        if C_RANGE[0] <= px <= C_RANGE[1] and C_RANGE[0] <= py <= C_RANGE[1]:
            return (px, py)

        return None


with open(INPUT_FILE_NAME, "r") as input_file:
    hails: List[Hail] = [
        Hail(*map(int, line.strip().replace(" @", ",").split(", ")))
        for line in input_file
    ]

# print(hails)

intersection_count = 0
for ai, hail_a in enumerate(hails):
    for bi, hail_b in enumerate(hails):
        if ai >= bi:
            continue

        intersection = hail_a.intersection(hail_b)
        if intersection is None:
            # print(f"{hail_a} (#{ai}) does not intersect {hail_b} (#{bi})")
            pass
        else:
            # print(f"{hail_a} (#{ai}) intersects {hail_b} (#{bi}) at {intersection}")
            intersection_count += 1

print(intersection_count)
