#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

possible_game_count = 0
possible_game_id_sum = 0
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        id_part, sets_part = line.strip().split(":", 1)
        game_id = int(id_part.split(" ")[1])
        sets = sets_part.strip().split("; ")
        possible = True
        for a_set in sets:
            available = dict(LIMITS)
            cubes = a_set.strip().split(", ")
            for cube in cubes:
                count, color = cube.strip().split(" ")
                count = int(count)
                available[color] -= count

            if any(available[color] < 0 for color in LIMITS):
                print(f"{game_id}: impossible")
                possible = False
                break

        if possible:
            possible_game_count += 1
            possible_game_id_sum += game_id
            print(f"{game_id}: possible")

print(f"Possible games: {possible_game_count}")
print(f"Sum of IDs: {possible_game_id_sum}")
