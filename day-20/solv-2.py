#!/usr/bin/env python3.12


"""
With help of visualisation here:
https://www.devtoolsdaily.com/graphviz/?#v2=N4IgJg9gLiBc4EsDmAnAhgBwBYAIDiOwAOgHYBGKEaYAxmgM5QCmKOA2vVpkwLw0IoaAGyYBdUqTC4OXDL36CR4kigC27Ttz4DhYyVA2z5OpaQCOYQ1oW7lqK3O2K95Mg+PPlYDO6e3SAG4GMtYmLgAe6iGONqYkpFhRmo5kEOHKZjS+qemk2Nlpyhj0BbkkZm7RvDnKAFZCpcoAZtLJ1YWkAF6djaQkllU8NX3hveVNYyQ+g8P9SUZDHST0ZmNkAWusM0uqSGMA1iXbZeFbbYtlAWcLs0JZx8pQqw+kNNdaswED57NQlT9LMA9F4kEgTEFgDYgsy1A73AFlJDghHKAKtG5LejvFJLJrTFGkfawkEYeEYsr7Z4Ekjhb7kx57EEoEhjLB0j5LMyM6lmFkg-bBan0KHUprsnEnbn00iqUYgsYSEiJHAAWgAfDg3uYsuqcP1JLhdWo8oaNd08iVdfsaAAaHBgKDmNy6h2keqqjVBO1-UgtD321R21CkChUWgMZisXVTO27O1fO2nLo9XUrUhqf0ocJ9Sy6igjf1XeOO8b+h12yF9Hy6yJ27CSdTRppBlCkFb+okhja6vGJ1QhqMagUyvYuzot-SFsAVgIVrB2xJ2w4L6c4SmEy0asxNcy5jXGmmDnBenDMwJHqBIYukO7+yKkJ7+1B2lqvI+Uislr5lqBL+gP50NRpSQUw1Z8cDFUh7BdDBYyvCDV15PoJl1YN+m7DVEnMWFdTuPtCR1DVyxwJEoJQojfxwCpAlNHBaxwYU2yPIJfWrLd4PvEgiULLA8kInAngnLjVl1NlSFpO94LQy9-Sxa9XEzfsVBZXUT0yBI9xwYpzFHDV6JhSQ2NPJTeX9UlCQMXV6jbDCcHWQJLI1MgyDtfo7UyRMUDtChvRctcSzFf1ZXExszXHBjZwYsw63nNdalc2CqLAcTdJIryqPiEhZSfdLaVIABfEB8qAA
"""


from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from math import lcm
from typing import Dict, List, Optional


# INPUT_FILE_NAME: str = "test-input"
# INPUT_FILE_NAME: str = "test-input-2"
INPUT_FILE_NAME: str = "input"


class PulseValue(Enum):
    LOW: int = 0
    HIGH: int = 1

    def __repr__(self) -> str:
        return "low" if self == PulseValue.LOW else "high"

    @property
    def high(self) -> bool:
        return self == PulseValue.HIGH


@dataclass
class Pulse:
    value: PulseValue
    source: str
    destination: str


class Module:
    def __init__(self, name: str, destinations: List[str]) -> None:
        self.name: str = name
        self.destinations: List[str] = destinations

    def pulse(self, pulse: Pulse) -> List[Pulse]:
        next_pulse_value = self.get_next_pulse_value(pulse)
        if next_pulse_value is None:
            return []

        return [Pulse(next_pulse_value, self.name, dest) for dest in self.destinations]

    def get_next_pulse_value(self, pulse: Pulse) -> Optional[PulseValue]:
        raise NotImplementedError()


class Debug(Module):
    def __str__(self) -> str:
        return f"[D: {self.name}]"

    def get_next_pulse_value(self, pulse: Pulse) -> Optional[PulseValue]:
        # print(f"{self.name}: {pulse}")
        pass


class Broadcaster(Module):
    NAME: str = "broadcaster"

    def get_next_pulse_value(self, pulse: Pulse) -> Optional[PulseValue]:
        return pulse.value

    def __str__(self) -> str:
        return f"[B: {self.name} -> {self.destinations}]"


class FlipFlop(Module):
    def __init__(self, name: str, destinations: List[str]) -> None:
        super().__init__(name, destinations)
        self.on: bool = False

    def __str__(self) -> str:
        return f"[FF: {self.name} -> {self.destinations}, on: {self.on}]"

    def get_next_pulse_value(self, pulse: Pulse) -> Optional[PulseValue]:
        if pulse.value.high:
            return None

        self.on ^= True
        return PulseValue.HIGH if self.on else PulseValue.LOW


class Conjunction(Module):
    def __init__(self, name: str, destinations: List[str]) -> None:
        super().__init__(name, destinations)
        self.recent: Dict[str, PulseValue] = {}
        self.decider = set(destinations) == {"rx"}
        self.loop_sizes: Dict[str, int] = {}

    def __str__(self) -> str:
        return f"[C: {self.name} -> {self.destinations}, recent: {self.recent}]"

    def set_step(self, step: int) -> None:
        self.step = step

    def add_input(self, input_name) -> None:
        self.recent[input_name] = PulseValue.LOW
        self.loop_sizes[input_name] = None

    def get_next_pulse_value(self, pulse: Pulse) -> Optional[PulseValue]:
        self.recent[pulse.source] = pulse.value

        if self.decider and pulse.value.high:
            self.loop_sizes[pulse.source] = self.step
            print(f"{self.name}: {pulse.source}={pulse.value} ({self.step})")

        return (
            PulseValue.LOW
            if all(p.high for p in self.recent.values())
            else PulseValue.HIGH
        )

    def get_loop_size(self) -> Optional[int]:
        if not self.decider:
            return None

        if any(v is None for v in self.loop_sizes.values()):
            return None

        return lcm(*self.loop_sizes.values())


modules = {}
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        name_part, destinations_part = line.strip().split(" -> ")
        destinations = destinations_part.split(", ")
        probably_name = name_part[1:]
        if name_part[0] == "%":
            modules[probably_name] = FlipFlop(probably_name, destinations)
        elif name_part[0] == "&":
            modules[probably_name] = Conjunction(probably_name, destinations)
        elif name_part == Broadcaster.NAME:
            modules[name_part] = Broadcaster(name_part, destinations)
        else:
            raise ValueError(f"Unknown module type: {line}")

generic_modules = {}
for name, module in modules.items():
    for destination in module.destinations:
        if not destination in modules:
            generic_modules[destination] = Debug(destination, [])
modules.update(generic_modules)

for name, module in modules.items():
    for destination in module.destinations:
        if isinstance(modules[destination], Conjunction):
            modules[destination].add_input(name)


def solve(modules: Dict[str, Module]) -> None:
    pulse_count = {PulseValue.LOW: 0, PulseValue.HIGH: 0}
    press_no = 1
    while True:
        pulses_to_process = deque([Pulse(PulseValue.LOW, "start", Broadcaster.NAME)])
        pulse_count[PulseValue.LOW] += 1
        while pulses_to_process:
            pulse = pulses_to_process.popleft()
            dest = modules[pulse.destination]

            if isinstance(dest, Conjunction):
                dest.set_step(press_no)

            new_pulses = dest.pulse(pulse)
            pulses_to_process.extend(new_pulses)

            if isinstance(dest, Conjunction):
                loop_size = dest.get_loop_size()
                if loop_size is not None:
                    print(f"Done: {loop_size=}")
                    return

            for new_pulse in new_pulses:
                pulse_count[new_pulse.value] += 1

        press_no += 1


solve(modules)
