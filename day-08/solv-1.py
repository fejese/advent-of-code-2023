#!/usr/bin/env python3

import re

# INPUT_FILE_NAME: str = "test-input"
# INPUT_FILE_NAME: str = "test-input-2"
INPUT_FILE_NAME: str = "input"

LINE_PATTERN = re.compile(r"([A-Z]+)\s*=\s*\(([A-Z]+),\s*([A-Z]+)\)")

nodes = {}
with open(INPUT_FILE_NAME, "r") as input_file:
    directions = [0 if c == "L" else 1 for c in input_file.readline().strip()]
    input_file.readline()
    for line in input_file:
        parts = LINE_PATTERN.match(line).groups()
        nodes[parts[0]] = (parts[1], parts[2])

current_node = "AAA"
steps = 0
while current_node != "ZZZ":
    direction = directions[steps % len(directions)]
    steps += 1
    next_node = nodes[current_node][direction]
    print(f"{steps}: {current_node} -> {next_node}")
    current_node = next_node

print(f"{steps=}")
