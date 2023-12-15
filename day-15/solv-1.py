#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


def get_hash(s: str) -> int:
    current_value = 0
    for c in s:
        current_value = ((current_value + ord(c)) * 17) % 256

    return current_value


with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        print(sum(get_hash(part) for part in line.strip().split(",")))
