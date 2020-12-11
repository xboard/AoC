#!/usr/bin/env python3
"""
Solves day 11 tasks of AoC 2020.

https://adventofcode.com/2020/day/11
"""

import argparse
import gzip
import copy
from os.path import dirname, realpath
from io import StringIO
from typing import List, Tuple, IO, Iterator, NewType
from pathlib import Path
from enum import Enum, auto

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"


class Task(Enum):
    """Task enumeration."""

    task1 = auto()
    task2 = auto()


class PositionStatus(Enum):
    """Position enumeration."""

    floor = "."
    empty = "L"
    occupied = "#"

    @classmethod
    def from_string(cls, seat: str) -> "PositionStatus":
        """Get Position from given string s."""
        for member in cls:
            if seat == member.value:
                return member
        raise NameError(f"{seat} is not a valid {cls}")


# Custom types
Layout = NewType("Layout", List[List[PositionStatus]])
Coordinate = NewType("Coordinate", Tuple[int, int])


def read_layout(input_io: IO) -> Layout:
    """Read layout from input."""
    layout = list()
    while line := input_io.readline():
        line = line.strip()
        layout.append(list(PositionStatus.from_string(s) for s in line))
    return Layout(layout)


def directions(layout: Layout, row: int, col: int) -> Iterator[Coordinate]:
    """
    Generate directions coordinates from a given row and col.

    Get coordinate of possible in all 8 directions (as described in task 2)
    until find a Seat.

    Parameters
    ----------
    layout: Layout
        Input layout.
    row: int
        row in layout to get direction from.
    col: int
        col in layout go get directions from.

    Return
    ------
    Iterator[Coordinate]
        coordinate of directions from (row, col).
    """
    num_rows = len(layout)
    num_cols = len(layout[0])

    def horizontal_directions() -> Iterator[Coordinate]:
        new_col = col - 1
        while new_col >= 0:
            yield Coordinate((row, new_col))
            if layout[row][new_col] != PositionStatus.floor:
                break
            new_col -= 1

        new_col = col + 1
        while new_col < num_cols:
            yield Coordinate((row, new_col))
            if layout[row][new_col] != PositionStatus.floor:
                break
            new_col += 1

    def vertical_directions() -> Iterator[Coordinate]:
        new_row = row - 1
        while new_row >= 0:
            yield Coordinate((new_row, col))
            if layout[new_row][col] != PositionStatus.floor:
                break
            new_row -= 1

        new_row = row + 1
        while new_row < num_rows:
            yield Coordinate((new_row, col))
            if layout[new_row][col] != PositionStatus.floor:
                break
            new_row += 1

    def diagonal_directions() -> Iterator[Coordinate]:
        new_row, new_col = row - 1, col - 1
        while new_row >= 0 and new_col >= 0:
            yield Coordinate((new_row, new_col))
            if layout[new_row][new_col] != PositionStatus.floor:
                break
            new_row -= 1
            new_col -= 1

        new_row, new_col = row + 1, col + 1
        while new_row < num_rows and new_col < num_cols:
            yield Coordinate((new_row, new_col))
            if layout[new_row][new_col] != PositionStatus.floor:
                break
            new_row += 1
            new_col += 1

        new_row, new_col = row + 1, col - 1
        while new_row < num_rows and new_col >= 0:
            yield Coordinate((new_row, new_col))
            if layout[new_row][new_col] != PositionStatus.floor:
                break
            new_row += 1
            new_col -= 1

        new_row, new_col = row - 1, col + 1
        while new_row >= 0 and new_col < num_cols:
            yield Coordinate((new_row, new_col))
            if layout[new_row][new_col] != PositionStatus.floor:
                break
            new_row -= 1
            new_col += 1

    yield from horizontal_directions()
    yield from vertical_directions()
    yield from diagonal_directions()


def apply_rule(layout: Layout, task: Task) -> Tuple[Layout, bool]:
    """
    Apply task rules to layout.

    Parameter
    ---------
    layout: Layout
        Input layout.
    task: Task
        From Task enum.

    Returns
    -------
    Layout: new layout after applying rules.
    bool: True if output layout differs from input layout.
    """
    num_rows = len(layout)
    if num_rows == 0:
        return layout, False
    num_cols = len(layout[0])

    def is_occupied(row: int, col: int) -> bool:
        if (0 <= row < num_rows) and (0 <= col < num_cols):
            if layout[row][col] == PositionStatus.occupied:
                return True
        return False

    deltas = [(-1, -1), (-1, 0), (0, -1), (-1, 1)]
    deltas += [(1, -1), (0, 1), (1, 0), (1, 1)]

    layout_resp = copy.deepcopy(layout)
    updated = False

    for row in range(num_rows):
        for col in range(num_cols):
            if layout[row][col] == PositionStatus.floor:
                continue
            if task == Task.task1:
                occ = [is_occupied(row + dr, col + dc) for (dr, dc) in deltas]
            elif task == Task.task2:
                dirs = directions(layout, row, col)
                occ = [is_occupied(dr, dc) for (dr, dc) in dirs]
            else:
                raise Exception("Task {task} invalid!")
            if layout[row][col] == PositionStatus.empty:
                if sum(occ) == 0:
                    layout_resp[row][col] = PositionStatus.occupied
                    updated = True
            elif layout[row][col] == PositionStatus.occupied:
                if (task == Task.task1 and sum(occ) >= 4) or (
                    task == Task.task2 and sum(occ) >= 5
                ):
                    layout_resp[row][col] = PositionStatus.empty
                    updated = True

    return layout_resp, updated


def task1(input_io: IO) -> int:
    """
    Solve task 1.

    Parameters
    ----------
    input_io: IO
        stream to seats.

    Return
    ------
    int
        number of seats end up occupied.

    """
    layout, updated = apply_rule(read_layout(input_io), Task.task1)
    while updated:
        layout, updated = apply_rule(layout, Task.task1)
    occ = [p for row in layout for p in row if p == PositionStatus.occupied]
    return len(occ)


def task2(input_io: IO) -> int:
    """
    Solve task 2.

    Parameters
    ----------
    input_io: IO
        stream to seats .

    Return
    ------
    int
        number of seats end up occupied..

    """
    layout, updated = apply_rule(read_layout(input_io), Task.task2)
    while updated:
        layout, updated = apply_rule(layout, Task.task2)
    occ = [p for row in layout for p in row if p == PositionStatus.occupied]
    return len(occ)


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
        num_occupied = task1(file)
        print(f"Task 1: {num_occupied} seats end up occupied.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        num_occupied = task2(file)
        print(f"Task 2: {num_occupied} seats end up occupied.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def input_stream() -> IO:
    """Input stream fixture."""
    return StringIO(
        """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
    )


def test_position_from_string():
    """Test Position.from_string."""
    assert PositionStatus.from_string("L") == PositionStatus.empty
    assert PositionStatus.from_string(".") == PositionStatus.floor
    assert PositionStatus.from_string("#") == PositionStatus.occupied


def test_read_layout():
    """Test read_layout."""
    layout = list(read_layout(input_stream()))
    assert len(layout) == 10
    assert len(layout[0]) == 10
    assert layout[0][0] == PositionStatus.empty
    assert layout[0][1] == PositionStatus.floor
    assert len([pos for pos in layout[6] if pos == PositionStatus.empty]) == 2
    occ = [p for row in layout for p in row if p == PositionStatus.occupied]
    assert len(occ) == 0


def test_apply_rule_task1():
    """Test apply rule for task 1."""
    layout = read_layout(input_stream())

    layout2, updt = apply_rule(layout, Task.task1)
    assert updt
    assert layout2[0][0] == PositionStatus.occupied
    occ = [pos for pos in layout2[0] if pos == PositionStatus.occupied]
    assert len(occ) == 7
    assert layout2[1][0] == PositionStatus.occupied
    occ = [pos for pos in layout2[1] if pos == PositionStatus.occupied]
    assert len(occ) == 9
    assert layout2[6][0] == PositionStatus.floor
    occ = [pos for pos in layout2[6] if pos == PositionStatus.occupied]
    assert len(occ) == 2

    layout3, updt = apply_rule(layout2, Task.task1)
    assert updt
    occ = [p for row in layout3 for p in row if p == PositionStatus.occupied]
    emp = [p for row in layout3 for p in row if p == PositionStatus.empty]
    assert len(occ) == 20
    assert len(emp) == 51


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    num_occupied = task1(input_stream())
    assert num_occupied == 37


def test_directions():
    """Test directions generator."""
    input_io = StringIO(
        """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#....."""
    )
    layout = read_layout(input_io)
    dirs = tuple(directions(layout, 4, 3))
    # print(dirs)
    assert len(dirs) == 23

    input_io = StringIO(
        """.............
.L.L.#.#.#.#.
............."""
    )
    layout = read_layout(input_io)
    dirs = tuple(directions(layout, 1, 1))
    print(dirs)
    assert len(dirs) == 9


def test_apply_rule_task2():
    """Test apply rule for task 2."""
    layout = read_layout(input_stream())

    layout2, updt = apply_rule(layout, Task.task2)
    assert updt
    assert layout2[0][0] == PositionStatus.occupied
    occ = [pos for pos in layout2[0] if pos == PositionStatus.occupied]
    assert len(occ) == 7
    assert layout2[1][0] == PositionStatus.occupied
    occ = [pos for pos in layout2[1] if pos == PositionStatus.occupied]
    assert len(occ) == 9
    assert layout2[6][0] == PositionStatus.floor
    occ = [pos for pos in layout2[6] if pos == PositionStatus.occupied]
    assert len(occ) == 2

    layout3, updt = apply_rule(layout2, Task.task2)
    assert updt
    occ = [p for row in layout3 for p in row if p == PositionStatus.occupied]
    emp = [p for row in layout3 for p in row if p == PositionStatus.empty]
    assert len(occ) == 7
    assert len(emp) == 64


def test_task2_with_example_input():
    """Test task2 with problem statement example."""
    num_occupied = task2(input_stream())
    assert num_occupied == 26


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        num_occupied = task1(file)
        assert num_occupied == 2468


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        num_occupied = task2(file)
        assert num_occupied == 2214
