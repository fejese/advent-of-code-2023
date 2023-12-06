#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    time_limit = int("".join(input_file.readline().strip().split()[1:]))
    distance_to_beat = int("".join(input_file.readline().strip().split()[1:]))


print(f"Processing: [{time_limit=}, {distance_to_beat=}]")
winning_options = 0
for button_time in range(1, time_limit):
    distance = (time_limit - button_time) * button_time
    # print(f"  Button time: {button_time}, distance: {distance}")
    if distance > distance_to_beat:
        winning_options += 1
print(f"  Winning options: {winning_options}")
