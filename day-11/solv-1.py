#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


with open(INPUT_FILE_NAME, "r") as input_file:
    omap = [list(l.strip()) for l in input_file.readlines()]

emap = []
for row in omap:
    emap.append(list(row))
    if "#" not in row:
        emap.append(list(row))

for x in range(len(omap[0]) - 1, -1, -1):
    if any(omap[y][x] == "#" for y in range(len(omap))):
        continue

    for row in emap:
        row.insert(x, ".")

galaxies = []
for y, row in enumerate(emap):
    for x, c in enumerate(row):
        if c == ".":
            continue
        galaxies.append((x, y))

distance = 0
for i, galaxy_i in enumerate(galaxies):
    for j, galaxy_j in enumerate(galaxies):
        if i >= j:
            continue
        distance += abs(galaxy_i[0] - galaxy_j[0]) + abs(galaxy_i[1] - galaxy_j[1])

print(f"Part 1: {distance}")
