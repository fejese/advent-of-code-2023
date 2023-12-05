#!/usr/bin/env python3

from dataclasses import dataclass

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


@dataclass
class Range:
    dst_start: int
    src_start: int
    length: int


class Map:
    def __init__(self, data: str):
        ranges = [
            Range(*[int(num) for num in line.split(" ")])
            for line in data.strip().split("\n")[1:]
        ]
        self.ranges = sorted(ranges, key=lambda r: r.src_start)

    def map(self, num: int) -> int:
        for rng in self.ranges:
            if num >= rng.src_start and num < (rng.src_start + rng.length):
                return num + rng.dst_start - rng.src_start
        return num


with open(INPUT_FILE_NAME, "r") as input_file:
    parts = input_file.read().split("\n\n")
    seeds = [int(x) for x in parts[0].split(" ")[1:]]

    maps = [Map(map_data) for map_data in parts[1:]]

    seeds_to_locations = {}
    for seed in seeds:
        num = seed
        for mapping in maps:
            num = mapping.map(num)

        seeds_to_locations[seed] = num

print(seeds_to_locations)
print(min(seeds_to_locations.values()))
