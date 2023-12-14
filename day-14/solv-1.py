#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


with open(INPUT_FILE_NAME, "r") as input_file:
    grid = [list(line.strip()) for line in input_file]

W = len(grid[0])
H = len(grid)
ROUNDED = "O"
CUBE = "#"
EMPTY = "."

[print("".join(line)) for line in grid]
print("rounded: ", sum(sum(1 if c == ROUNDED else 0 for c in line) for line in grid))
print("cube: ", sum(sum(1 if c == CUBE else 0 for c in line) for line in grid))
print("empty: ", sum(sum(1 if c == EMPTY else 0 for c in line) for line in grid))
# print(",".join([f"{x},{y}" for y, line in enumerate(grid) for x, c in enumerate(line) if c == CUBE]))
print()

movement = True
while movement:
    movement = False
    for x in range(W):
        for y in range(H - 1):
            if (grid[y + 1][x], grid[y][x]) == (ROUNDED, EMPTY):
                movement = True
                grid[y + 1][x], grid[y][x] = (EMPTY, ROUNDED)

[print("".join(line)) for line in grid]
print("rounded: ", sum(sum(1 if c == ROUNDED else 0 for c in line) for line in grid))
print("cube: ", sum(sum(1 if c == CUBE else 0 for c in line) for line in grid))
print("empty: ", sum(sum(1 if c == EMPTY else 0 for c in line) for line in grid))
# print(",".join([f"{x},{y}" for y, line in enumerate(grid) for x, c in enumerate(line) if c == CUBE]))
print()

total_load = 0
for x in range(W):
    for y in range(H):
        if grid[y][x] == ROUNDED:
            load = H - y
            total_load += load

print(f"{total_load=}")
