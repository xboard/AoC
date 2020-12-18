#!/usr/bin/env python3
"""
Solves day 17 tasks of AoC 2020.

https://adventofcode.com/2020/day/17
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import Tuple, List, Set, IO, Iterator, NewType, cast
from pathlib import Path
from dataclasses import dataclass

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"

State = NewType("State", Set[Tuple[int, int, int]])


def read_initial_state(input_io: IO) -> State:
    row = 0
    actives = set()
    while line := input_io.readline():
        for col, char in enumerate(line.strip()):
            if char == "#":
                actives.add((row, col, 0))
        row += 1
    return State(actives)


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
    state = read_initial_state(input_io)
    for _ in range(6):
        candidates = State(set())
        for x, y, z in state:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        candidates.add((x + dx, y + dy, z + dz))

        actives = State(set())
        for x, y, z in candidates:
            num_actives = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        if dx == dy == dz == 0:
                            continue
                        if (x + dx, y + dy, z + dz) in state:
                            num_actives += 1

            if (x, y, z) in state and num_actives in [2, 3]:
                actives.add((x, y, z))
            if (x, y, z) not in state and num_actives == 3:
                actives.add((x, y, z))
        state = State(actives)
    return len(state)


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
    pass


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
        answer = task1(file)
        print(f"Task 1: answer is {answer}.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        answer = task2(file)
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
    state = read_initial_state(input_stream())
    assert len(state) == 5
    assert (1, 2, 0) in state
    assert (0, 0, 0) not in state
    assert (0, 1, 0) in state
    assert (1, 1, 0) not in state
    assert (2, 1, 0) in state


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    answer = task1(input_stream())
    assert answer == 112


# def test_task2_with_example_input():
#     """Test task2 with problem statement example."""
#     questions_solved = task2(input_stream())
#     assert questions_solved == 6


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        answer = task1(file)
        assert answer == 426


# def test_task2_with_input_file():
#     """Test task2 with given input file (gziped)."""
#     with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
#         val = task2(file)
#         assert val == 777
