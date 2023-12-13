#!/usr/bin/env python3

from typing import List


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    maps = [
        [l.strip() for l in m.splitlines()] for m in input_file.read().split("\n\n")
    ]


def get_horizontal_value(m: List[str]) -> int:
    for value in range(1, len(m)):
        compare_size = min(value, len(m) - value)
        top = m[value - compare_size : value]
        bottom = m[value : value + compare_size]

        if top == list(reversed(bottom)):
            return value

    return None


def flip(m: List[str]) -> List[str]:
    flipped = []
    for x in range(len(m[0])):
        row = ""
        for y in range(len(m)):
            row += m[y][x]
        flipped.append(row)
    return flipped


total = 0
for m in maps:
    value = get_horizontal_value(m)
    if value is None:
        value = get_horizontal_value(flip(m))
    else:
        value *= 100

    total += value

print(total)
