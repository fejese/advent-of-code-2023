#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

num_words = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

total = 0
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        first = -1
        last = -1
        for i, c in enumerate(line):
            if c in "0123456789":
                if first == -1:
                    first = int(c)
                last = int(c)
                continue

            for num, num_word in enumerate(num_words, 1):
                if line[i:i+len(num_word)] == num_word:
                    if first == -1:
                        first = num
                    last = num
        num = first * 10 + last
        print(f"{line.strip()} -> {first}, {last} => {num}")
        total += num

print(total)
