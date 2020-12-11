#!/usr/bin/env python3
"""
Solves day 12 tasks of AoC 2020.

https://adventofcode.com/2020/day/12
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import List, Union, IO, Iterator, Protocol, cast
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"


class Turn(Enum):
    """Enumerate values for Turn."""

    LEFT = 10
    RIGHT = 20


class Direction(Enum):
    """Enumerate values for Direction."""

    WEST = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    FWD = 4


@dataclass(frozen=True)
class Instruction:
    """Class representing an Instruction."""

    action: Union[Direction, Turn]
    value: int


class StateProtocol(Protocol):
    """Protocol for State classes."""

    def apply(self, instr: Instruction):
        """Apply instruction to current state."""
        raise NotImplementedError

    @property
    def manhatam_distance(self) -> int:
        """Calculate Manhatam distance from origin."""
        raise NotImplementedError


@dataclass
class StateTask1(StateProtocol):
    """Represent ship state for task 1."""

    steering: Direction
    north: int
    east: int

    def __post_init__(self):
        """Validate if steering has been correctly initialzed."""
        if self.steering == Direction.FWD:
            raise ValueError("Steering can't be FORWARD.")

    def apply(self, instr: Instruction):
        """Apply instruction to current state."""
        if isinstance(instr.action, Turn):
            self._rotate(cast("Turn", instr.action), instr.value)
        else:
            self._translate(cast("Direction", instr.action), instr.value)

    def _rotate(self, turn: Turn, degrees: int):
        if degrees % 90 != 0:
            raise ValueError(
                f"Parameter degrees must be a multiple of 90. Got {degrees}."
            )
        spin = degrees / 90
        if turn == Turn.LEFT:
            self.steering = Direction((self.steering.value - spin + 4) % 4)
        if turn == Turn.RIGHT:
            self.steering = Direction((self.steering.value + spin) % 4)
        if self.steering == Direction.FWD:
            raise ValueError("Steering can't be FORWARD")

    def _translate(self, direction: Direction, amount: int):
        if direction == Direction.EAST:
            self.east += amount
        elif direction == Direction.WEST:
            self.east -= amount
        elif direction == Direction.NORTH:
            self.north += amount
        elif direction == Direction.SOUTH:
            self.north -= amount
        else:  # direction == Direction.FWD
            self._forward(amount)

    def _forward(self, amount: int):
        if self.steering == Direction.NORTH:
            self.north += amount
        elif self.steering == Direction.SOUTH:
            self.north -= amount
        elif self.steering == Direction.EAST:
            self.east += amount
        elif self.steering == Direction.WEST:
            self.east -= amount
        else:
            raise ValueError(
                f"Invalid state. Direction FORWARD, steering = {self.steering}"
            )

    @property
    def manhatam_distance(self) -> int:
        """Calculate Manhatam distance from origin."""
        return abs(self.north) + abs(self.east)


@dataclass
class StateTask2(StateProtocol):
    """Represent ship state for Task 2."""

    # (North, East)
    waypoint: List[int]
    position: List[int]

    def apply(self, instr: Instruction):
        """Apply instruction to current state."""
        if isinstance(instr.action, Turn):
            self._rotate(cast("Turn", instr.action), instr.value)
        else:
            self._translate(cast("Direction", instr.action), instr.value)

    def _rotate(self, turn: Turn, degrees: int):
        if degrees % 90 != 0:
            raise ValueError(
                f"Parameter degrees must be a multiple of 90. Got {degrees}."
            )
        spin = degrees / 90
        while spin > 0:
            if turn == Turn.LEFT:
                self._rotate_left()
            elif turn == Turn.RIGHT:
                self._rotate_right()
            spin -= 1

    def _rotate_left(self):
        north, east = self.waypoint
        self.waypoint = [east, -north]

    def _rotate_right(self):
        north, east = self.waypoint
        self.waypoint = [-east, north]

    def _translate(self, direction: Direction, amount: int):
        if direction == Direction.NORTH:
            self.waypoint[0] += amount
        elif direction == Direction.SOUTH:
            self.waypoint[0] -= amount
        elif direction == Direction.EAST:
            self.waypoint[1] += amount
        elif direction == Direction.WEST:
            self.waypoint[1] -= amount
        else:  # direction == Direction.FWD
            self._forward(amount)

    def _forward(self, amount: int):
        self.position[0] += amount * self.waypoint[0]
        self.position[1] += amount * self.waypoint[1]

    @property
    def manhatam_distance(self) -> int:
        """Calculate Manhatam distance from origin."""
        return abs(self.position[0]) + abs(self.position[1])


def read_instructions(input_io: IO) -> Iterator[Instruction]:
    """
    Iterate Instructions in stream.

    Parameters
    ----------
    input_io: IO
        instructions stream.

    Return
    ------
    Iterator[Instruction]
    """
    while line := input_io.readline():
        line = line.strip()
        if line[0] == "L":
            yield Instruction(Turn.LEFT, int(line[1:]))
        elif line[0] == "R":
            yield Instruction(Turn.RIGHT, int(line[1:]))
        elif line[0] == "N":
            yield Instruction(Direction.NORTH, int(line[1:]))
        elif line[0] == "S":
            yield Instruction(Direction.SOUTH, int(line[1:]))
        elif line[0] == "E":
            yield Instruction(Direction.EAST, int(line[1:]))
        elif line[0] == "W":
            yield Instruction(Direction.WEST, int(line[1:]))
        elif line[0] == "F":
            yield Instruction(Direction.FWD, int(line[1:]))


def solve(instructions: Iterator[Instruction], state: StateProtocol) -> int:
    """
    Solve task 1 or 2.

    Parameters
    ----------
    input_io: IO
        stream to all .

    Return
    ------
    int
        .

    """
    for instruction in instructions:
        state.apply(instruction)

    return state.manhatam_distance


def task1(input_io: IO) -> int:
    """
    Solve task 1.

    Parameters
    ----------
    input_io: IO
        stream to all .

    Return
    ------
    int
        .

    """
    return solve(read_instructions(input_io), StateTask1(Direction.EAST, 0, 0))


def task2(input_io: IO) -> int:
    """
    Solve task 2.

    Parameters
    ----------
    input_io: IO
        stream to all .

    Return
    ------
    int
        .

    """
    return solve(read_instructions(input_io), StateTask2([1, 10], [0, 0]))


def get_input_file() -> Path:
    """
    Parse arguments passed to script.

    Return:
    Path
        path to gziped file for this problem.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("GZIPED_FILE", help="gziped file for this problem")
    args = parser.parse_args()
    return Path(args.GZIPED_FILE)


def main() -> None:
    """Run script."""
    input_file = get_input_file()
    with gzip.open(input_file, "rt", encoding="ascii") as file:
        distance = task1(file)
        print(f"Task 1: Manhattan distance is {distance}.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        distance = task2(file)
        print(f"Task 2: Manhattan distance is {distance}.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def input_stream() -> IO:
    """Input stream fixture."""
    return StringIO(
        """F10
N3
F7
R90
F11"""
    )


def test_input_stream_state_statewp():
    """Test read_instructions, State and StateWP."""
    state_t1 = StateTask1(Direction.EAST, 0, 0)
    state_t2 = StateTask2([1, 10], [0, 0])

    instructions = tuple(read_instructions(input_stream()))
    assert state_t1.manhatam_distance == 0

    assert instructions[0] == Instruction(Direction.FWD, 10)
    state_t1.apply(instructions[0])
    state_t2.apply(instructions[0])
    assert state_t1.north == 0 and state_t1.east == 10
    assert state_t2.waypoint == [1, 10]
    assert state_t2.position == [10, 100]

    assert instructions[1] == Instruction(Direction.NORTH, 3)
    state_t1.apply(instructions[1])
    state_t2.apply(instructions[1])
    assert state_t1.north == 3 and state_t1.east == 10
    assert state_t2.waypoint == [4, 10]
    assert state_t2.position == [10, 100]

    assert instructions[2] == Instruction(Direction.FWD, 7)
    state_t1.apply(instructions[2])
    state_t2.apply(instructions[2])
    assert state_t1.north == 3 and state_t1.east == 17
    assert state_t2.waypoint == [4, 10]
    assert state_t2.position == [38, 170]

    assert instructions[3] == Instruction(Turn.RIGHT, 90)
    state_t1.apply(instructions[3])
    state_t2.apply(instructions[3])
    assert state_t1.north == 3 and state_t1.east == 17
    assert state_t2.waypoint == [-10, 4]
    assert state_t2.position == [38, 170]

    assert instructions[4] == Instruction(Direction.FWD, 11)
    state_t1.apply(instructions[4])
    state_t2.apply(instructions[4])
    assert state_t1.north == -8 and state_t1.east == 17
    assert state_t2.waypoint == [-10, 4]
    assert state_t2.position == [-72, 214]


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    distance = task1(input_stream())
    assert distance == 25


def test_task2_with_example_input():
    """Test task2 with problem statement example."""
    distance = task2(input_stream())
    assert distance == 286


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        distance = task1(file)
        assert distance == 1457


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        distance = task2(file)
        assert distance == 106860
