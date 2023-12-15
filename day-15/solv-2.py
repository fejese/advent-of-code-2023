#!/usr/bin/env python3


from __future__ import annotations


from collections import OrderedDict, defaultdict
from dataclasses import dataclass


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"
DEBUG: bool = False


def get_hash(s: str) -> int:
    current_value = 0
    for c in s:
        current_value = ((current_value + ord(c)) * 17) % 256

    return current_value


@dataclass
class Lense:
    label: str
    focal_length: int

    @classmethod
    def from_instruction(cls, instruction: str) -> Lense:
        parts = instruction.split("=")
        return cls(parts[0], int(parts[1]))

    def __str__(self) -> str:
        return f"[{self.label} {self.focal_length}]"

    def calculate_power(self, box_number: int, lense_position: int) -> int:
        power = (box_number + 1) * lense_position * self.focal_length
        if DEBUG:
            print(
                f"{self.label}: {box_number + 1} * {lense_position} * {self.focal_length} = {power}"
            )
        return power


class Box:
    def __init__(self) -> None:
        self._lenses = OrderedDict()

    def init(self, number: int) -> None:
        self._number = number

    def add(self, lense: Lense) -> None:
        self._lenses[lense.label] = lense

    def remove(self, label: str) -> None:
        if label in self._lenses:
            del self._lenses[label]

    def __str__(self) -> str:
        return " ".join(str(lense) for lense in self._lenses.values())

    def calculate_power(self, number: int) -> int:
        power = 0
        for lense_position, lense in enumerate(self._lenses.values(), 1):
            power += lense.calculate_power(number, lense_position)

        return power

    def has_items(self) -> bool:
        return not not self._lenses


class Boxes:
    def __init__(self) -> None:
        self._boxes = defaultdict(Box)

    def process(self, instruction: str) -> None:
        if "=" in instruction:
            lense = Lense.from_instruction(instruction)
            self._boxes[get_hash(lense.label)].add(lense)
        else:
            label = instruction.rstrip("-")
            self._boxes[get_hash(label)].remove(label)

        if DEBUG:
            print(f'After "{instruction}":')
            [
                print(f"Box {number}: {box}")
                for number, box in self._boxes.items()
                if box.has_items()
            ]

    def calculate_power(self) -> int:
        power = 0
        for number, box in self._boxes.items():
            power += box.calculate_power(number)

        return power


boxes = Boxes()
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        if "-" not in line:
            continue
        for instruction in line.strip().split(","):
            boxes.process(instruction)

total_power = boxes.calculate_power()
print(f"{total_power=}")
