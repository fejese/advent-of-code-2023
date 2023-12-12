#!/usr/bin/env python3.12

import re
from typing import Any, List, Set, Tuple
from functools import cache


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


def report(
    pattern: str, start_pos: int, lengths: List[int], level: int, comment: str = ""
) -> None:
    # print(f"{level * '  '}{pattern=} {start_pos=} {lengths=}", end="")
    # if comment:
    #     print(f" ({comment})")
    # else:
    #     print()
    pass


def report_result(result: Set[str], level: int, comment: str = "") -> Set[str]:
    # print(f"{level * '  '}=> {result=}", end="")
    # if comment:
    #     print(f" ({comment})")
    # else:
    #     print()

    return result


@cache
def has_functioning_spring(pattern: str, start_pos: int) -> bool:
    return "#" in pattern[start_pos:]


@cache
def all_potentially_functioning(pattern: str, pos: int, length: int) -> bool:
    return all(c != "." for c in pattern[pos : pos + length])


@cache
def functioning_ends(pattern: str, end_pos: int) -> bool:
    return end_pos == len(pattern) or pattern[end_pos] != "#"


@cache
def can_place(pattern, pos: int, length: int) -> bool:
    return all_potentially_functioning(pattern, pos, length) and functioning_ends(
        pattern, pos + length
    )


@cache
def get_position_combination(
    pattern: str, start_pos: int, lengths: Tuple[int, ...], level: int = 1
) -> int:
    report(pattern, start_pos, lengths, level)

    if not lengths:
        if has_functioning_spring(pattern, start_pos):
            return report_result(0, level, "# not covered")
        else:
            return report_result(1, level, "done")

    if start_pos >= len(pattern):
        return report_result(0, level, "start_pos out of bounds")

    if pattern[start_pos] == ".":
        result = get_position_combination(pattern, start_pos + 1, lengths, level + 1)
        return report_result(result, level, "removing trailing .")

    if start_pos + lengths[0] > len(pattern):
        return report_result(0, level, "first length out of bounds")

    if start_pos + sum(lengths) + len(lengths) - 1 > len(pattern):
        return report_result(0, level, "lengths out of bounds")

    combinations = 0
    for pos in range(start_pos, len(pattern) - lengths[0] + 1):
        if can_place(pattern, pos, lengths[0]):
            combinations += get_position_combination(
                pattern, pos + lengths[0] + 1, tuple(lengths[1:]), level + 1
            )
        if pattern[pos] == "#":
            break
    return report_result(combinations, level)


def process_line(line: str) -> int:
    parts = line.split()
    broken_lengths = [int(n) for n in parts[1].split(",")] * 5
    springs = "?".join([parts[0]] * 5)
    position_combination_count = get_position_combination(
        springs, 0, tuple(broken_lengths)
    )
    print(f"  ==> {position_combination_count=}")
    return position_combination_count


with open(INPUT_FILE_NAME, "r") as input_file:
    print(sum(process_line(line.strip()) for line in input_file.readlines()))
