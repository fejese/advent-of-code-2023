#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
# EXPANSION_FACTOR: int = 10-1
# EXPANSION_FACTOR: int = 100-1
INPUT_FILE_NAME: str = "input"
EXPANSION_FACTOR: int = 1000000 - 1


with open(INPUT_FILE_NAME, "r") as input_file:
    omap = [list(l.strip()) for l in input_file.readlines()]

all_empty_rows = [y for y, row in enumerate(omap) if "#" not in row]
all_empty_cols = [
    x for x in range(len(omap[0])) if all(omap[y][x] == "." for y in range(len(omap)))
]

galaxies = []
for y, row in enumerate(omap):
    for x, c in enumerate(row):
        if c == ".":
            continue
        galaxies.append((x, y))

distance = 0
for i, gi in enumerate(galaxies):
    for j, gj in enumerate(galaxies):
        if i >= j:
            continue

        distance += (
            abs(gi[0] - gj[0])
            + sum(
                EXPANSION_FACTOR
                for col in all_empty_cols
                if min(gi[0], gj[0]) < col < max(gi[0], gj[0])
            )
            + abs(gi[1] - gj[1])
            + sum(
                EXPANSION_FACTOR
                for row in all_empty_rows
                if min(gi[1], gj[1]) < row < max(gi[1], gj[1])
            )
        )


print(f"Part 2: {distance}")
