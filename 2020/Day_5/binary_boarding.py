#!/usr/bin/env python3
"""
Solves day 5 tasks of AoC 2020.

https://adventofcode.com/2020/day/5
"""

import gzip
from typing import List, Iterator, NewType, cast
from pathlib import Path

INPUT_FILE_PATH = Path(".") / "input.txt.gz"
ROW_LENGTH = 7

SeatId = NewType("SeatId", int)
SeatPath = NewType("SeatPath", str)


def read_paths(file_path: Path) -> Iterator[SeatPath]:
    """
    Iterate over all seats in file_path.

    Parameters
    ----------
    input_path: Path
        Path to gziped input file with all seats path.

    Return
    ------
    Iterator[SeatPath]
        Iterator to seat paths read.
    """
    with gzip.open(file_path, "rt") as file:
        while line := cast("str", file.readline()):
            yield SeatPath(line.strip())


def get_id_from_path(path: SeatPath) -> SeatId:
    """
    Convert a SeatPath to a SeatId.

    From the problem descriptions we notice that paths are a binary
    representation of seat id where letters 'F' and 'L' represents 0 and
    letters 'B' and 'R' representing 1. We translate letters to their
    binary counterparts and get row and column in decimal, multiply row
    by 8 adding column to get the seat id.

    Parameters
    ----------
    path: SeatPath
        string representing a path to a seat.

    Returns
    -------
    SeatId: int
        id of this seat.
    """
    row = int(path[:ROW_LENGTH].replace("F", "0").replace("B", "1"), 2)
    col = int(path[ROW_LENGTH:].replace("L", "0").replace("R", "1"), 2)
    return SeatId(row * 8 + col)


def task1(file_path: Path) -> SeatId:
    """
    Solve task 1.

    Parameters
    ----------
    input_path: Path
        Path to gziped input file with all seats path.

    Return
    ------
    SeatId: int
        highest seat id found in input file.

    """
    highest = SeatId(0)
    for path in read_paths(file_path):
        seat_id = get_id_from_path(path)
        highest = max(highest, seat_id)
    return highest


def task2(file_path: Path) -> SeatId:
    """
    Solve task 2.

    Parameters
    ----------
    input_path: Path
        Path to gziped input file with all seats path.

    Return
    ------
    SeatId: int
        integer (ranging from 0 to 1023) representing my seat id
    """
    seats: List[SeatId] = []

    for path in read_paths(file_path):
        seats.append(get_id_from_path(path))
    seats.sort()

    for i in range(1, len(seats) - 1):
        if seats[i - 1] + 1 == seats[i] - 1:
            return SeatId(seats[i] - 1)
    raise Exception("Seat not found!")


def main() -> None:
    """Run script."""
    highest_seat_id = task1(INPUT_FILE_PATH)
    assert highest_seat_id == 822
    print(f"Task 1: highest seat id is {highest_seat_id}.")

    my_seat_id = task2(INPUT_FILE_PATH)
    assert my_seat_id == 705
    print(f"Task 2: my_seat_id = {my_seat_id}.")


if __name__ == "__main__":
    main()
