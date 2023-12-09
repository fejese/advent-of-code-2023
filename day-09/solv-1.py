#!/usr/bin/env python3

from typing import List


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


def predict(nums: List[int]) -> int:
    if all(n == 0 for n in nums):
        return 0

    next_nums = [nums[i] - nums[i - 1] for i in range(1, len(nums))]
    next_predict = predict(next_nums)
    return nums[-1] + next_predict


predict_sum = 0
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        nums = [int(c) for c in line.strip().split()]
        predicted = predict(nums)
        print(f"{nums=} => {predicted}")
        predict_sum += predict(nums)

print(f"{predict_sum=}")
