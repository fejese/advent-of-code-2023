#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    times = [int(t) for t in input_file.readline().strip().split()[1:]]
    distances = [int(d) for d in input_file.readline().strip().split()[1:]]


margin_of_error = 1
for time_limit, distance_to_beat in zip(times, distances):
    print(f"Processing: [{time_limit=}, {distance_to_beat=}]")
    winning_options = 0
    for button_time in range(1, time_limit):
        distance = (time_limit - button_time) * button_time
        # print(f"  Button time: {button_time}, distance: {distance}")
        if distance > distance_to_beat:
            winning_options += 1
    print(f"  Winning options: {winning_options}")
    margin_of_error *= winning_options

print(f"Margin of error: {margin_of_error}")
