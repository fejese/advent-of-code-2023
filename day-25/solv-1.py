#!/usr/bin/env python3

from collections import defaultdict
from itertools import takewhile
from typing import Dict, Set, Tuple, Optional

INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

nodes = set()
edges = set()
neighbours = defaultdict(set)
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        parts = line.strip().split(":")
        node = parts[0]
        line_neighbours = parts[1].strip().split()
        nodes.add(node)
        for neighbour in line_neighbours:
            nodes.add(neighbour)
            edges.add(tuple(sorted([node, neighbour])))
            neighbours[node].add(neighbour)
            neighbours[neighbour].add(node)

print(f"{len(nodes)=}")
# print(f"{nodes=}")
print(f"{len(edges)=}")
# print(f"{edges=}")
print(f"{len(neighbours)=}")
# print(f"{neighbours=}")


def get_two_parts(
    neighbours: Dict[str, Set[str]],
    edge_a: Tuple[str, str],
    edge_b: Tuple[str, str],
    edge_c: Tuple[str, str],
) -> Optional[Tuple[Set[str], Set[str]]]:
    # print(f"get_two_parts: {edge_a=}, {edge_b=}, {edge_c=}")
    edges_to_ignore = {edge_a, edge_b, edge_c, tuple(reversed(edge_a)), tuple(reversed(edge_b)), tuple(reversed(edge_c))}
    nodes_left = set(neighbours.keys())
    parts = []

    for _ in range(2):
        # print(f"{(nodes_left)=}")
        if not nodes_left:
            return None

        first_node = nodes_left.pop()
        # print(f"    {(first_node)=}")
        part = {first_node}
        to_process = {first_node}

        while to_process:
            # print(f"    {(to_process)=}")
            new_to_process = set()
            for node in to_process:
                # print(f"        {(node)=}")
                for neighbour in neighbours[node]:
                    # print(f"        {(neighbour)=}")
                    if (node, neighbour) in edges_to_ignore:
                        continue
                    if neighbour not in part:
                        part.add(neighbour)
                        new_to_process.add(neighbour)
                        nodes_left.remove(neighbour)
            to_process = new_to_process
        parts.append(part)

    if nodes_left:
        return None

    return tuple(parts)


# print(get_two_parts(neighbours, ("hfx", "pzl"), ("bvb", "cmg"), ("jqt", "nvd")))



edges = sorted(edges)

found = False
for ei, edge_i in enumerate(edges):
    if edge_i[0] > edge_i[1]:
        continue
    for ej, edge_j in enumerate(edges):
        if edge_j[0] > edge_j[1]:
            continue
        if edge_j <= edge_i:
            continue
        for ek, edge_k in enumerate(edges):
            if edge_k[0] > edge_k[1]:
                continue
            if edge_k <= edge_j:
                continue
            parts = get_two_parts(neighbours, edge_i, edge_j, edge_k)
            if parts is None:
                continue
            print(f"{len(parts[0])=} x {len(parts[1])=} = {len(parts[0]) * len(parts[1])=}")
            found = True
            break

        if found:
            break
    if found:
        break
