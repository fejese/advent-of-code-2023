#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input-7"
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
start_shape = possible_s.pop()

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


inside_count = 0
inside = False


def p(y, yt, msg):
    global inside
    global inside_count
    if y >= yt:
        print(msg, f"{inside=}, {inside_count=}")


for x in range(len(pipe_map[0])):
    inside = False
    line_start = None
    for y in range(len(pipe_map)):
        pos = (x, y)
        p(y, 60, f"{pos=}")
        if pos in distances:
            c = start_shape if pos == (start_x, start_y) else pipe_map[y][x]
            p(y, 60, f"  {c=}")

            if c == "|":
                p(y, 60, f"  => Noop")
                continue

            if c == "-":
                inside = not inside
                p(y, 60, f"  => Noop")
                continue

            if not line_start:
                line_start = c
                continue

            if {line_start, c} in [set("FJ"), set("7L")]:
                inside = not inside
            line_start = None
        else:
            if inside:
                print(f"{pos=}")
                inside_count += 1

print(f"{inside_count=}")
