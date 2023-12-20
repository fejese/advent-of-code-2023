#!/usr/bin/env python3


from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


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
        print(f"{self.name}: {pulse}")


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

    def __str__(self) -> str:
        return f"[C: {self.name} -> {self.destinations}, recent: {self.recent}]"

    def add_input(self, input_name) -> None:
        self.recent[input_name] = PulseValue.LOW

    def get_next_pulse_value(self, pulse: Pulse) -> Optional[PulseValue]:
        self.recent[pulse.source] = pulse.value

        return (
            PulseValue.LOW
            if all(p.high for p in self.recent.values())
            else PulseValue.HIGH
        )


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


pulse_count = {PulseValue.LOW: 0, PulseValue.HIGH: 0}
for _ in range(1000):
    pulses_to_process = deque([Pulse(PulseValue.LOW, "start", Broadcaster.NAME)])
    pulse_count[PulseValue.LOW] += 1
    while pulses_to_process:
        pulse = pulses_to_process.popleft()
        new_pulses = modules[pulse.destination].pulse(pulse)
        pulses_to_process.extend(new_pulses)

        for new_pulse in new_pulses:
            pulse_count[new_pulse.value] += 1

print(pulse_count)
print(pulse_count[PulseValue.HIGH] * pulse_count[PulseValue.LOW])
