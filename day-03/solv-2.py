#!/usr/bin/env python3

import re

from collections import defaultdict


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

NUM_PATTERN = re.compile(r"(^|(?<!\d))(\d+)($|(?!\d))")
SYM_PATTERN = re.compile(r"[^.\d]")

with open(INPUT_FILE_NAME, "r") as input_file:
    lines = [l.strip() for l in input_file.readlines()]


def get_gears(lines, start_x, end_x, y):
    neighbours = {}
    if y > 0:
        for x in range(max(0, start_x - 1), min(end_x + 1, len(lines[y]))):
            neighbours[(x, y - 1)] = lines[y - 1][x]
    if end_x < len(lines[y]):
        neighbours[(end_x, y)] = lines[y][end_x]
    if y + 1 < len(lines):
        for x in range(max(0, start_x - 1), min(end_x + 1, len(lines[y]))):
            neighbours[(x, y + 1)] = lines[y + 1][x]
    if start_x > 0:
        neighbours[(start_x - 1, y)] = lines[y][start_x - 1]

    return {coord for coord, symbol in neighbours.items() if symbol == "*"}


numbers_per_gear = defaultdict(list)
for y, line in enumerate(lines):
    print(f"Processing line {y}: {line} ...")
    for number_match in NUM_PATTERN.finditer(line):
        print(f"  Found number match: {number_match}")
        number = int(number_match.group())
        print(f"    Number: {number}")
        print(f"    Start: {number_match.start()}")
        print(f"    End: {number_match.end()}")
        gears = get_gears(lines, number_match.start(), number_match.end(), y)
        print(f"    Gears: {gears}")
        for gear in gears:
            numbers_per_gear[gear].append(number)

ratio_sum = 0
for gear, numbers in numbers_per_gear.items():
    print(f"Gear {gear}: {numbers}")
    if len(numbers) != 2:
        print("  Not really a gear")
        continue

    ratio = numbers[0] * numbers[1]
    print(f"  Ratio: {ratio}")
    ratio_sum += ratio


print(f"Ratio sum: {ratio_sum}")
