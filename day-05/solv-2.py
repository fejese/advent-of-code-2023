#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


@dataclass
class Range:
    start: int
    length: int


@dataclass
class MapRange:
    dst_start: int
    src_start: int
    length: int


class Map:
    def __init__(self, data: str) -> None:
        ranges = [
            MapRange(*[int(num) for num in line.split(" ")])
            for line in data.strip().split("\n")[1:]
        ]
        self.ranges = sorted(ranges, key=lambda r: r.src_start)

    def map(self, rng: Range) -> List[Range]:
        mapped_ranges = []
        for mrng in self.ranges:
            if rng.start >= mrng.src_start and rng.start < (
                mrng.src_start + mrng.length
            ):
                if rng.start + rng.length <= mrng.src_start + mrng.length:
                    mapped_ranges.append(
                        Range(rng.start + mrng.dst_start - mrng.src_start, rng.length)
                    )
                    rng = None
                    break
                else:
                    new_length = mrng.length - (rng.start - mrng.src_start)
                    mapped_ranges.append(
                        Range(
                            rng.start + mrng.dst_start - mrng.src_start,
                            new_length,
                        )
                    )
                    rng = Range(mrng.src_start + mrng.length, rng.length - new_length)
            if rng.start < mrng.src_start and rng.start + rng.length >= mrng.src_start:
                new_length = rng.length - (mrng.src_start - rng.start)
                mapped_ranges.append(
                    Range(
                        mrng.dst_start,
                        new_length,
                    )
                )
                rng = Range(rng.start, rng.length - new_length)

        if rng is not None:
            mapped_ranges.append(rng)
        return mapped_ranges


with open(INPUT_FILE_NAME, "r") as input_file:
    parts = input_file.read().split("\n\n")
    range_nums = [int(x) for x in parts[0].split(" ")[1:]]
    ranges = [
        Range(range_nums[i], range_nums[i + 1]) for i in range(0, len(range_nums), 2)
    ]
    # print(ranges)

    maps = [Map(map_data) for map_data in parts[1:]]

    for mapping in maps:
        new_ranges = []
        for rng in ranges:
            new_ranges.extend(mapping.map(rng))
        ranges = new_ranges
        # print(ranges)

ranges = sorted(ranges, key=lambda r: r.start)
print(ranges[0].start)
