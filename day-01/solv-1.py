#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

total = 0
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        first = -1
        last = -1
        for c in line:
            if c in "0123456789":
                if first == -1:
                    first = int(c)
                last = int(c)
        num = first * 10 + last
        print(f"{line.strip()} -> {first}, {last} => {num}")
        total += num

print(total)
