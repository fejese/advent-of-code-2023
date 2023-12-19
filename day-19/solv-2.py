#!/usr/bin/env python3

from __future__ import annotations

import re

from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional


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

    @property
    def value(self) -> int:
        return self.x + self.m + self.a + self.s

    def __hash__(self) -> int:
        return hash((self.x, self.m, self.a, self.s))


@dataclass
class ItemRange:
    start: Item
    end: Item

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    @property
    def size(self) -> int:
        return (
            (abs(self.end.x - self.start.x) + 1)
            * (abs(self.end.m - self.start.m) + 1)
            * (abs(self.end.a - self.start.a) + 1)
            * (abs(self.end.s - self.start.s) + 1)
        )


class Operand(Enum):
    LT: str = "<"
    GT: str = ">"


@dataclass
class Condition:
    attr: str
    operand: Operand
    threshold: int

    @classmethod
    def from_str(cls, s: str) -> Rule:
        parts = RULE_PATTERN.match(s).groups()
        return cls(parts[0], Operand(parts[1]), int(parts[2]))

    def evaluate(self, item: Item) -> bool:
        attr_value = getattr(item, self.attr)
        if self.operand == Operand.LT:
            return attr_value < self.threshold
        if self.operand == Operand.GT:
            return attr_value > self.threshold
        raise NotImplementedError(f"Unknown operator {self.operand}")

    @property
    def split_lower_end(self) -> int:
        if self.operand == Operand.LT:
            return self.threshold - 1
        if self.operand == Operand.GT:
            return self.threshold
        raise NotImplementedError(f"Unknown operator {self.operand}")

    @property
    def split_higher_start(self) -> int:
        if self.operand == Operand.LT:
            return self.threshold
        if self.operand == Operand.GT:
            return self.threshold + 1
        raise NotImplementedError(f"Unknown operator {self.operand}")


@dataclass
class Rule:
    target: str
    condition: Optional[Condition] = None

    @classmethod
    def from_str(cls, s: str) -> Rule:
        parts = s.split(":")
        if len(parts) == 1:
            return cls(parts[0], None)

        return cls(parts[1], Condition.from_str(parts[0]))

    def process(self, item: Item) -> Optional[str]:
        if not self.condition or self.condition.evaluate(item):
            return self.target
        return None

    def process_range(self, item_range: ItemRange) -> Dict[ItemRange, Optional[str]]:
        condition = self.condition
        if not condition:
            return {item_range: self.target}

        start_result = self.process(item_range.start)
        if item_range.start == item_range.end:
            return {item_range: start_result}

        end_result = self.process(item_range.end)
        lower_end = Item(
            **{
                attr: (
                    condition.split_lower_end
                    if condition.attr == attr
                    else getattr(item_range.end, attr)
                )
                for attr in "xmas"
            }
        )
        higher_start = Item(
            **{
                attr: (
                    condition.split_higher_start
                    if condition.attr == attr
                    else getattr(item_range.start, attr)
                )
                for attr in "xmas"
            }
        )
        return {
            ItemRange(item_range.start, lower_end): start_result,
            ItemRange(higher_start, item_range.end): end_result,
        }


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

    def process(self, item_range: ItemRange) -> Dict[ItemRange, str]:
        to_process = [item_range]
        results = {}

        # print(f"        [W:{self.name}] {to_process=}")
        for rule in self.rules:
            # print(f"            [R:{rule}] {to_process=}")
            new_to_process = []
            for item_range in to_process:
                rule_results = rule.process_range(item_range)
                # print(f"            {rule_results=}")
                for new_item_range, result in rule_results.items():
                    if result is None:
                        new_to_process.append(new_item_range)
                    else:
                        results[new_item_range] = result
            to_process = new_to_process

        return results


with open(INPUT_FILE_NAME, "r") as input_file:
    input_parts = input_file.read().split("\n\n")
    workflows = [W.from_line(line.strip()) for line in input_parts[0].splitlines()]

workflow_map = {w.name: w for w in workflows}
item_ranges_to_process = {
    ItemRange(Item(1, 1, 1, 1), Item(4000, 4000, 4000, 4000)): "in"
}
accepted_ranges = []

while item_ranges_to_process:
    # print(item_ranges_to_process)
    new_item_ranges_to_process = {}
    for item_range, workflow_name in item_ranges_to_process.items():
        results = workflow_map[workflow_name].process(item_range)

        # print(f"    {item_range=}, {workflow_name=} => {results=}")
        for new_item_range, new_workflow_name in results.items():
            if new_workflow_name == ACCEPTED:
                accepted_ranges.append(new_item_range)
            elif new_workflow_name == REJECTED:
                continue
            else:
                new_item_ranges_to_process[new_item_range] = new_workflow_name

    item_ranges_to_process = new_item_ranges_to_process

print(sum(r.size for r in accepted_ranges))
