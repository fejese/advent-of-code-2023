#!/usr/bin/env python3

import re

from collections import defaultdict


INPUT_FILE_NAME: str = "test-input"
# INPUT_FILE_NAME: str = "input"

NUM_PATTERN = re.compile(r"\b\d+\b")

cards = defaultdict(int)

with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        line = line.strip()
        print(f"Processing line: {line}")
        card_part, numbers_part = line.split(": ")
        card_num = int(NUM_PATTERN.search(card_part).group())
        cards[card_num] += 1

        winning_part, have_part = [p.strip() for p in numbers_part.split(" | ")]

        winning_numbers = set(int(m) for m in NUM_PATTERN.findall(winning_part))
        print(f"  winning numbers: {winning_numbers}")
        have_numbers = set(int(m) for m in NUM_PATTERN.findall(have_part))
        print(f"  have numbers: {have_numbers}")

        matches = winning_numbers.intersection(have_numbers)
        print(f"  matches: {matches}")

        new_cards = list(range(card_num + 1, card_num + len(matches) + 1))
        print(f"  new cards: {new_cards}")
        for i in new_cards:
            cards[i] += cards[card_num]

        print(f"  => {cards}")

total_num_cards = sum(cards.values())
print(f"Total number of cards: {total_num_cards}")
