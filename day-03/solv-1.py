#!/usr/bin/env python3

import re

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

NUM_PATTERN = re.compile(r"(^|(?<!\d))(\d+)($|(?!\d))")
SYM_PATTERN = re.compile(r"[^.\d]")

with open(INPUT_FILE_NAME, "r") as input_file:
    lines = [l.strip() for l in input_file.readlines()]


def get_neighbours(lines, start_x, end_x, y):
    neighbours = ""
    if y > 0:
        neighbours += lines[y - 1][max(0, start_x - 1) : end_x + 1]
    if end_x < len(lines[y]):
        neighbours += lines[y][end_x]
    if y + 1 < len(lines):
        neighbours += "".join(reversed(lines[y + 1][max(0, start_x - 1) : end_x + 1]))
    if start_x > 0:
        neighbours += lines[y][start_x - 1]
    return neighbours


nums_next_to_symbol = 0
for y, line in enumerate(lines):
    print(f"Processing line {y}: {line} ...")
    for number_match in NUM_PATTERN.finditer(line):
        print(f"  Found number match: {number_match}")
        number = int(number_match.group())
        print(f"    Number: {number}")
        print(f"    Start: {number_match.start()}")
        print(f"    End: {number_match.end()}")
        neighbours = get_neighbours(lines, number_match.start(), number_match.end(), y)
        print(f"    Neighbours: {neighbours}")
        symbol_match = SYM_PATTERN.search(neighbours) is not None
        print(f"    Symbol match: {symbol_match}")
        if not symbol_match:
            continue

        nums_next_to_symbol += number

print(f"Number of numbers next to a symbol: {nums_next_to_symbol}")
