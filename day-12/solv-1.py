#!/usr/bin/env python3

import re
from typing import Any, List, Set


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


def report(
    pattern: str, start_pos: int, lengths: List[int], level: int, comment: str = ""
) -> None:
    print(f"{level * '  '}{pattern=} {start_pos=} {lengths=}", end="")
    if comment:
        print(f" ({comment})")
    else:
        print()
    pass


def report_result(result: Set[str], level: int, comment: str = "") -> Set[str]:
    print(f"{level * '  '}=> {result=}", end="")
    if comment:
        print(f" ({comment})")
    else:
        print()

    return result


def get_position_combination(
    pattern: str, start_pos: int, lengths: List[int], level: int = 1
) -> Set[str]:
    report(pattern, start_pos, lengths, level)

    if not lengths:
        if "#" in pattern[start_pos:]:
            return report_result(set(), level, "# not covered")
        else:
            return report_result(set("F"), level, "done")

    if start_pos >= len(pattern):
        return report_result(set(), level, "start_pos out of bounds")

    if pattern[start_pos] == ".":
        result = get_position_combination(pattern, start_pos + 1, lengths, level + 1)
        return report_result(result, level, "removing trailing .")

    if start_pos + lengths[0] > len(pattern):
        return report_result(set(), level, "first length out of bounds")

    if start_pos + sum(lengths) + len(lengths) - 1 > len(pattern):
        return report_result(set(), level, "lengths out of bounds")

    first_positions = set()
    for pos in range(start_pos, len(pattern) - lengths[0] + 1):
        if all(c != "." for c in pattern[pos : pos + lengths[0]]) and (
            pos + lengths[0] == len(pattern) or pattern[pos + lengths[0]] != "#"
        ):
            first_positions.add(str(pos))
        if pattern[pos] == "#":
            break
    report_result(first_positions, level, "first positions")

    combinations = set()
    for first_position in first_positions:
        second_positions = get_position_combination(
            pattern, int(first_position) + lengths[0] + 1, lengths[1:], level + 1
        )
        for second_position in second_positions:
            combinations.add(f"{first_position}_{second_position}")

    return report_result(combinations, level)


def process_line(line: str) -> int:
    parts = line.split()
    broken_lengths = [int(n) for n in parts[1].split(",")]
    position_combination = get_position_combination(parts[0], 0, broken_lengths)
    position_combination_count = len(position_combination)
    print(f"  ==> {position_combination_count=}")
    return position_combination_count


with open(INPUT_FILE_NAME, "r") as input_file:
    print(sum(process_line(line.strip()) for line in input_file.readlines()))
