#!/usr/bin/env python3

from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

CARD_MAP = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
}


@dataclass
class Hand:
    hand: Tuple[int, int, int, int, int]
    typ: Tuple[int, str]
    bid: int


def parse_hand(hand: str) -> Tuple[int, int, int, int, int]:
    cards = []
    for card in hand:
        if card in CARD_MAP:
            cards.append(CARD_MAP[card])
        else:
            cards.append(int(card))
    return tuple(cards)


def get_type(hand: str) -> int:
    print(f"Getting type for {hand}")
    freq = defaultdict(int)
    for card in hand:
        freq[card] += 1
    print(f"  {freq=}")

    counts = sorted(freq.values(), reverse=True)
    print(f"  {counts=}")

    if counts[0] == 5:
        return (7, "five of a kind")

    if counts[0] == 4:
        return (6, "four of a kind")

    if counts[0] == 3:
        if counts[1] == 2:
            return (5, "full house")
        else:
            return (4, "three of a kind")

    if counts[0] == 2:
        if counts[1] == 2:
            return (3, "two pairs")
        else:
            return (2, "one pair")

    return (1, "high card")


hands = []
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        hand, bid_str = line.strip().split()
        bid = int(bid_str)
        hands.append(Hand(parse_hand(hand), get_type(hand), bid))

hands = sorted(hands, key=lambda h: (h.typ, h.hand))
print(hands)
winnings = 0
for rank, hand in enumerate(hands, 1):
    print(f"{hand=} {rank=}")
    winnings += rank * hand.bid

print(winnings)
