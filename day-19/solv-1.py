#!/usr/bin/env python3

from __future__ import annotations

import re

from dataclasses import dataclass
from typing import Callable, List


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

RULE_PATTERN: re.Pattern = re.compile(r"([a-z])([<>])(\d+)")

ACCEPTED: str = "A"
REJECTED: str = "R"


@dataclass
class Item:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_line(cls, line: str) -> Item:
        parts = line.strip("{").strip("}").split(",")
        argv = {}
        for part in parts:
            key, val = part.split("=")
            argv[key] = int(val)
        return cls(**argv)

    @property
    def value(self) -> int:
        return self.x + self.m + self.a + self.s


@dataclass
class Rule:
    condition: Callable[[Item], bool]
    target: str

    @classmethod
    def from_str(cls, s: str) -> Rule:
        parts = s.split(":")
        if len(parts) == 1:
            return cls(lambda _: True, parts[0])

        condition_parts = RULE_PATTERN.match(parts[0]).groups()
        if condition_parts[1] == "<":
            condition = lambda item: getattr(item, condition_parts[0]) < int(
                condition_parts[2]
            )
        elif condition_parts[1] == ">":
            condition = lambda item: getattr(item, condition_parts[0]) > int(
                condition_parts[2]
            )
        else:
            raise ValueError(f"Invalid condition {condition_parts}")

        return cls(condition, parts[1])


@dataclass
class W:
    name: str
    rules: List[I]

    @classmethod
    def from_line(cls, line: str) -> W:
        parts = line.split("{")
        name = parts[0]
        rules = parts[1].rstrip("}").split(",")
        return cls(name, [Rule.from_str(r) for r in rules])

    def process(self, item: Item) -> Item:
        for rule in self.rules:
            if rule.condition(item):
                return rule.target
        else:
            item.a += 1
        return item


with open(INPUT_FILE_NAME, "r") as input_file:
    input_parts = input_file.read().split("\n\n")
    workflows = [W.from_line(line.strip()) for line in input_parts[0].splitlines()]
    items = [Item.from_line(line.strip()) for line in input_parts[1].splitlines()]


workflow_map = {w.name: w for w in workflows}

total_value = 0
for item in items:
    workflow = "in"
    while workflow != ACCEPTED and workflow != REJECTED:
        workflow = workflow_map[workflow].process(item)

    if workflow == ACCEPTED:
        value = item.value
        print(f"{item} -> {value}")
        total_value += value

print(f"Total value: {total_value}")
