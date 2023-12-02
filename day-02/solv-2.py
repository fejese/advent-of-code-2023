#!/usr/bin/env python3

from collections import defaultdict

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

power_sum = 0
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        id_part, sets_part = line.strip().split(":", 1)
        game_id = int(id_part.split(" ")[1])
        sets = sets_part.strip().split("; ")
        used = defaultdict(int)
        for a_set in sets:
            cubes = a_set.strip().split(", ")
            for cube in cubes:
                count, color = cube.strip().split(" ")
                count = int(count)
                used[color] = max(count, used[color])

        power = used["red"] * used["green"] * used["blue"]
        print(f"{game_id}: {used['red']}x{used['green']}x{used['blue']}={power}")
        power_sum += power

print(power_sum)
