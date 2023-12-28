#!/usr/bin/env python3.12

import cProfile

from typing import List, Tuple, Optional, Set, Dict
from functools import cache


# INPUT_FILE_NAME: str = "test-input-2"
INPUT_FILE_NAME: str = "input"

C = Tuple[int, int]
PATH = "."
FOREST = "#"


def get_nodes_and_roads(grid: Tuple[str]) -> Tuple[List[C], Set[C]]:
    roads = set()
    nodes = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == FOREST:
                continue
            road_neighbours = 0
            for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                next_pos = (x + dx, y + dy)
                if not (0 <= next_pos[0] < len(grid[0])):
                    continue
                if not (0 <= next_pos[1] < len(grid)):
                    continue
                next_char = grid[next_pos[1]][next_pos[0]]
                if next_char != FOREST:
                    road_neighbours += 1
            if road_neighbours == 2:
                roads.add((x, y))
            else:
                nodes.append((x, y))

    return nodes, roads


# @cache
def get_distance(roads: Set[C], pos_a: C, pos_b: C) -> Optional[int]:
    distance = None
    visited: Set[C] = set()
    to_visit: List[C] = [pos_a]

    distance = 1
    while to_visit:
        to_visit_new: List[C] = []
        for pos in to_visit:
            visited.add(pos)
            for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                next_pos = (pos[0] + dx, pos[1] + dy)
                if next_pos == pos_b:
                    return distance
                if next_pos in visited:
                    continue
                if next_pos not in roads:
                    continue
                to_visit_new.append(next_pos)
        to_visit = to_visit_new
        distance += 1

    return None


def get_edges(node_map: Dict[C, int], roads: Set[C]) -> Dict[Tuple[int, int], int]:
    edges = {}
    for pos_a, node_a in node_map.items():
        for pos_b, node_b in node_map.items():
            if node_a >= node_b:
                continue
            distance = get_distance(roads, pos_a, pos_b)
            if distance is not None:
                edges[(node_a, node_b)] = distance
                edges[(node_b, node_a)] = distance
    return edges


CACHE: Dict[Tuple[int, int], int] = {}


def get_longest_path(
    edges: Dict[Tuple[int, int], int], node: int, visited: int, goal_node: int
) -> int:
    if node == goal_node:
        return 0

    global CACHE
    cache_key = (node, visited)
    if cache_key not in CACHE:
        valid_edges = {
            (edge_start, edge_end): edge_length
            for (edge_start, edge_end), edge_length in edges.items()
            if edge_start == node and visited & edge_end == 0
        }
        max_path_length = -1
        for (edge_start, edge_end), edge_length in valid_edges.items():
            sub_length = get_longest_path(edges, edge_end, visited | node, goal_node)
            if sub_length < 0:
                continue
            sub_length += edge_length
            if sub_length > max_path_length:
                max_path_length = sub_length

        CACHE[cache_key] = max_path_length

    return CACHE[cache_key]


def main() -> None:
    with open(INPUT_FILE_NAME, "r") as input_file:
        grid = tuple(line.strip() for line in input_file)

    nodes: List[C]
    roads: Set[C]
    nodes, roads = get_nodes_and_roads(grid)
    # print(f"{nodes=}")
    # print(f"roads={sorted(roads)}")
    start_pos: C = nodes[0]
    goal_pos: C = nodes[-1]
    node_map = {node: 2**i for i, node in enumerate(nodes)}
    node_number_map = {
        node_number: node_pos for node_pos, node_number in node_map.items()
    }
    start_node = node_map[start_pos]
    goal_node = node_map[goal_pos]
    print(f"{node_map=}")
    edges = get_edges(node_map, roads)
    print(f"{edges=}")

    print(f"{len(node_map)=}")
    print(f"{len(edges)=}")
    print(f"start: {start_pos}/{start_node}")
    print(f"goal: {goal_pos}/{goal_node}")

    longest_path_length = get_longest_path(edges, start_node, 0, goal_node)
    print(f"{longest_path_length=}")


# cProfile.run("main()", sort="tottime")

main()

# 6502
