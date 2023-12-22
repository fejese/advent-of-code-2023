#!/usr/bin/env python3

from collections import defaultdict

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

bricks = []
cubes = {}
with open(INPUT_FILE_NAME, "r") as input_file:
    brick_id = 0
    for line in input_file:
        brick_name = f"brick-{brick_id:05}"
        brick_parts = line.strip().split("~")
        brick_start = tuple(int(p) for p in brick_parts[0].split(","))
        brick_end = tuple(int(p) for p in brick_parts[1].split(","))

        if any(brick_start[i] > brick_end[i] for i in range(3)):
            raise ValueError(f"Invalid brick: {line}")

        bricks.append((brick_start, brick_end, brick_name))
        for xt in range(brick_start[0], brick_end[0] + 1):
            for yt in range(brick_start[1], brick_end[1] + 1):
                for zt in range(brick_start[2], brick_end[2] + 1):
                    cubes[(xt, yt, zt)] = brick_name
        brick_id += 1


moving = True
moving_rounds = 0
brick_moves = 0
while moving:
    moving_rounds += 1
    moving = False

    for brick_i, brick in enumerate(bricks):
        brick_moves += 1
        brick_start, brick_end, brick_name = brick
        bottom = brick_start[2]
        depth = 0
        if bottom > 1:
            settled = False
            while not settled:
                if bottom - depth == 1:
                    break
                for xt in range(brick_start[0], brick_end[0] + 1):
                    for yt in range(brick_start[1], brick_end[1] + 1):
                        if (xt, yt, bottom - depth - 1) in cubes:
                            settled = True
                            break
                    if settled:
                        break
                if not settled:
                    depth += 1

        if depth > 0:
            moving = True
            for zt in range(brick_start[2], brick_end[2] + 1):
                for xt in range(brick_start[0], brick_end[0] + 1):
                    for yt in range(brick_start[1], brick_end[1] + 1):
                        del cubes[(xt, yt, zt)]
                        cubes[(xt, yt, zt - depth)] = brick_name
            bricks[brick_i] = (
                (brick_start[0], brick_start[1], brick_start[2] - depth),
                (brick_end[0], brick_end[1], brick_end[2] - depth),
                brick_name,
            )

print(f"Moving rounds: {moving_rounds}")
print(f"Brick moves: {brick_moves}")

supported_by = defaultdict(set)
for brick_start, brick_end, brick_name in bricks:
    top = max(brick_start[2], brick_end[2])
    for xt in range(brick_start[0], brick_end[0] + 1):
        for yt in range(brick_start[1], brick_end[1] + 1):
            if (xt, yt, top + 1) in cubes:
                supported_by[cubes[(xt, yt, top + 1)]].add(brick_name)

required = set()
for supported, supporters in supported_by.items():
    # print(f"{supported} is supported by {supporters} bricks")
    if len(supporters) == 1:
        required.update(supporters)
        # print(f"Marking {supporter} as required")

print(f"Required bricks: {len(required)}")

all_bricks = set([brick_name for _, _, brick_name in bricks])
# print(f"All bricks: {sorted(all_bricks)}")

removable_bricks = all_bricks - required
print(f"Part 1 - Removable bricks: {len(removable_bricks)}")

# part 2

on_floor = {name for name in all_bricks if name not in supported_by}


def num_fall_if_removed(removed):
    global on_floor
    unsupported = {
        k
        for k, v in supported_by.items()
        if not v - removed and k not in removed | on_floor
    }
    if not unsupported:
        return 0
    return len(unsupported) + num_fall_if_removed(removed | unsupported)


all_falling = sum(num_fall_if_removed({brick_name}) for brick_name in all_bricks)
print(f"Part 2 - All falling: {all_falling}")
