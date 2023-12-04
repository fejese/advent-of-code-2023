#!/usr/bin/env python3

import re

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

NUM_PATTERN = re.compile(r"\b\d+\b")

total_points = 0
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        card_part, numbers_part = line.split(": ")
        winning_part, have_part = [p.strip() for p in numbers_part.split(" | ")]

        winning_numbers = set(int(m) for m in NUM_PATTERN.findall(winning_part))
        print(f"  winning numbers: {winning_numbers}")
        have_numbers = set(int(m) for m in NUM_PATTERN.findall(have_part))
        print(f"  have numbers: {have_numbers}")

        matches = winning_numbers.intersection(have_numbers)
        print(f"  matches: {matches}")

        if len(matches):
            points = 2 ** (len(matches) - 1)
        else:
            points = 0

        print(f"  points: {points}")

        total_points += points

print(f"Total points: {total_points}")
