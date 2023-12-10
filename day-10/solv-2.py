#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input-4"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    pipe_map = [l.strip() for l in input_file.readlines()]


start_y, start_line = [(y, l) for y, l in enumerate(pipe_map) if "S" in l][0]
start_x = [x for x, c in enumerate(pipe_map[start_y]) if c == "S"][0]

distances = {}
distances[(start_x, start_y)] = 0
to_process = []
possible_s = set("|-7FLJ")
if pipe_map[start_y - 1][start_x] in "|7F":
    to_process.append((start_x, start_y - 1))
    possible_s.difference_update(set("-F7"))
if pipe_map[start_y + 1][start_x] in "|LJ":
    to_process.append((start_x, start_y + 1))
    possible_s.difference_update(set("-JL"))
if pipe_map[start_y][start_x - 1] in "-LF":
    to_process.append((start_x - 1, start_y))
    possible_s.difference_update(set("|J7"))
if pipe_map[start_y][start_x + 1] in "-J7":
    to_process.append((start_x + 1, start_y))
    possible_s.difference_update(set("|FL"))

print(f"{possible_s=}")

curr_distance = 0
while len(to_process) > 0:
    curr_distance += 1
    new_to_process = []
    for pos in to_process:
        x, y = pos
        if pipe_map[y][x] in ".S":
            continue
        elif pipe_map[y][x] == "|":
            new_to_process.append((x, y - 1))
            new_to_process.append((x, y + 1))
        elif pipe_map[y][x] == "-":
            new_to_process.append((x - 1, y))
            new_to_process.append((x + 1, y))
        elif pipe_map[y][x] == "L":
            new_to_process.append((x + 1, y))
            new_to_process.append((x, y - 1))
        elif pipe_map[y][x] == "J":
            new_to_process.append((x - 1, y))
            new_to_process.append((x, y - 1))
        elif pipe_map[y][x] == "7":
            new_to_process.append((x - 1, y))
            new_to_process.append((x, y + 1))
        elif pipe_map[y][x] == "F":
            new_to_process.append((x + 1, y))
            new_to_process.append((x, y + 1))
    to_process = [c for c in new_to_process if c not in distances]
    for pos in to_process:
        distances[pos] = curr_distance

print_map = {
    "|": "┃",
    "-": "━",
    "L": "┗",
    "J": "┛",
    "7": "┓",
    "F": "┏",
    ".": " ",
}


for y in range(len(pipe_map)):
    for x in range(len(pipe_map[0])):
        if (x, y) == (start_x, start_y):
            print("S", end="")
        elif (x, y) in distances:
            print(print_map[pipe_map[y][x]], end="")
        else:
            print(".", end="")
    print()
