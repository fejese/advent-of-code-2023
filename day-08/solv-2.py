#!/usr/bin/env python3.10

import re
import math

from collections import defaultdict

# INPUT_FILE_NAME: str = "test-input-3"
INPUT_FILE_NAME: str = "input"

LINE_PATTERN = re.compile(r"([0-9A-Z]+)\s*=\s*\(([0-9A-Z]+),\s*([0-9A-Z]+)\)")

nodes = {}
with open(INPUT_FILE_NAME, "r") as input_file:
    directions = input_file.readline().strip()
    input_file.readline()
    for line in input_file:
        parts = LINE_PATTERN.match(line).groups()
        nodes[parts[0]] = {"L": parts[1], "R": parts[2]}


starting_nodes = [k for k in nodes.keys() if k.endswith("A")]
loop_lengths = {}
steps = 0
current_nodes = list(starting_nodes)
while len(loop_lengths) < len(starting_nodes):
    direction = directions[steps % len(directions)]
    steps += 1
    current_nodes = [nodes[current_node][direction] for current_node in current_nodes]
    for starting_node, current_node in zip(starting_nodes, current_nodes):
        if current_node.endswith("Z") and starting_node not in loop_lengths:
            loop_lengths[starting_node] = steps


print(len(directions))
print(f"{loop_lengths=}")
min_steps = math.lcm(*loop_lengths.values())
print(f"{min_steps=}")
