#!/usr/bin/env python3
"""
Solves day 5 tasks of AoC 2020.

https://adventofcode.com/2020/day/5
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import List, Iterator, IO, NewType, cast
from pathlib import Path

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"
ROW_LENGTH = 7

SeatId = NewType("SeatId", int)
SeatPath = NewType("SeatPath", str)


def read_paths(input_io: IO) -> Iterator[SeatPath]:
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
    while line := cast("str", input_io.readline()):
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


def task1(input_io: IO) -> SeatId:
    """
    Solve task 1.

    Parameters
    ----------
    input_io: IO
        Stream of seats path.

    Return
    ------
    SeatId: int
        highest seat id found in input file.

    """
    highest = SeatId(0)
    for path in read_paths(input_io):
        seat_id = get_id_from_path(path)
        highest = max(highest, seat_id)
    return highest


def task2(input_io: IO) -> SeatId:
    """
    Solve task 2.

    Parameters
    ----------
    input_io: IO
        Stream of seats path.

    Returns
    -------
    SeatId: int
        integer (ranging from 0 to 1023) representing my seat id

    Raises
    ------
    LookupError
        when SeatId coundn't be found.
    """
    seats: List[SeatId] = []

    for path in read_paths(input_io):
        seats.append(get_id_from_path(path))
    seats.sort()

    for i in range(1, len(seats) - 1):
        if seats[i - 1] + 1 == seats[i] - 1:
            return SeatId(seats[i] - 1)
    raise LookupError("Seat not found!")


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
        highest_seat_id = task1(cast("IO", file))
        print(f"Task 1: highest seat id is {highest_seat_id}.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        my_seat_id = task2(cast("IO", file))
        print(f"Task 2: my_seat_id = {my_seat_id}.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def input_stream() -> IO:
    """Input stream fixture."""
    return StringIO(
        """BFFFBBFRRR
        FFFBBBFRRR
        BBFFBBFRLL"""
    )


def test_read_paths():
    """Test read_read_paths."""
    i = 0
    for path in read_paths(input_stream()):
        assert path is not None
        assert len(path) == 10
        i += 1
    assert i == 3


def test_get_id_from_path():
    """Test conversion to SeatId from a SeatPath."""
    assert get_id_from_path(SeatPath("BFFFBBFRRR")) == SeatId(567)
    assert get_id_from_path(SeatPath("FFFBBBFRRR")) == SeatId(119)
    assert get_id_from_path(SeatPath("BBFFBBFRLL")) == SeatId(820)


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        highest_seat_id = task1(cast("IO", file))
        assert highest_seat_id == 822


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        questions_solved = task2(file)
        assert questions_solved == 705
