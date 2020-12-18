#!/usr/bin/env python3
"""
Solves day 17 tasks of AoC 2020.

https://adventofcode.com/2020/day/17
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import Tuple, IO, Set
from pathlib import Path
from enum import Enum, auto

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"

Dimension = Tuple[int, int, int, int]
State = Set[Dimension]


class Task(Enum):
    """Enumerate tasks."""

    Task1 = auto()
    Task2 = auto()


def read_initial_state(input_io: IO) -> State:
    """
    Read initial state

    Parameters
    ----------
    input_io: IO
        stream to initial state.

    Return
    ------
    State:
        initial State.
    """
    row = 0
    actives = set()
    while line := input_io.readline():
        for col, char in enumerate(line.strip()):
            if char == "#":
                actives.add((row, col, 0, 0))
        row += 1
    return actives


def dim_iterator(task: Task) -> Dimension:
    """Iterates of variable dimensions"""
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if task == Task.Task2:
                    for dw in [-1, 0, 1]:
                        yield (dx, dy, dz, dw)
                else:
                        yield (dx, dy, dz, 0)


def solve(input_io: IO, task: Task) -> int:
    """
    Solve task 1.

    Parameters
    ----------
    input_io: IO
        stream to initial state.

    Return
    ------
    int
        number of active cubes.

    """
    state = read_initial_state(input_io)
    for _ in range(6):
        candidates: State = set()
        for x, y, z, w in state:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        if task == Task.Task2:
                            for dw in [-1, 0, 1]:
                                candidates.add((x + dx, y + dy, z + dz, w + dw))
                        else:
                            candidates.add((x + dx, y + dy, z + dz, 0))

        actives: State = set()
        for x, y, z, w in candidates:
            num_actives = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        for dw in [-1, 0, 1]:
                            if dx == dy == dz == dw == 0:
                                continue
                            if (x + dx, y + dy, z + dz, w + dw) in state:
                                num_actives += 1

            if (x, y, z, w) in state and num_actives in [2, 3]:
                actives.add((x, y, z, w))
            if (x, y, z, w) not in state and num_actives == 3:
                actives.add((x, y, z, w))
        state = actives
    return len(state)


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
        answer = solve(file, Task.Task1)
        print(f"Task 1: answer is {answer}.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        answer = solve(file, Task.Task2)
        print(f"Task 2: answer is {answer}.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def input_stream() -> IO:
    """Input stream fixture."""
    return StringIO(
        """.#.
..#
###"""
    )


def test_read_cubes():
    """Test read_cubes function."""
    state = read_initial_state(input_stream())
    assert len(state) == 5
    assert (1, 2, 0, 0) in state
    assert (0, 0, 0, 0) not in state
    assert (0, 1, 0, 0) in state
    assert (1, 1, 0, 0) not in state
    assert (2, 1, 0, 0) in state

def test_dim_iterator():
    """ Test dim_iterator function """
    iter = tuple(dim_iterator(Task.Task1))
    assert len(iter) == 27
    assert iter[0] == (-1, -1, -1, 0)
    iter = tuple(dim_iterator(Task.Task2))
    assert len(iter) == 81
    assert iter[0] == (-1, -1, -1, -1)


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    answer = solve(input_stream(), Task.Task1)
    assert answer == 112


def test_task2_with_example_input():
    """Test task2 with problem statement example."""
    answer = solve(input_stream(), Task.Task2)
    assert answer == 848


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        answer = solve(file, Task.Task1)
        assert answer == 426


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        answer = solve(file, Task.Task2)
        assert answer == 1892
