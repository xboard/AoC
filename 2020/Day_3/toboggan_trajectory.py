#!/usr/bin/env python3
"""
Solves day 3 tasks of AoC 2020.

https://adventofcode.com/2020/day/3
"""

import argparse
import gzip
from io import StringIO
from os.path import dirname, realpath
from typing import Tuple, Optional, IO
from pathlib import Path
from functools import reduce

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"


def solve_task(input_io: IO, slope: Tuple[int, int]) -> int:
    """
    Solves task 1: number of trees for slope right 3 down 1.

    Parameters
    ----------
    input_io: IO
        Map stream.

    slope: (slope_right: int, slope_down: int)
        Slope to use from top to botton.


    Returns
    -------
    int
        Number of trees '#' in path from top to bottom.
    """

    def go_down(amount: int) -> Optional[str]:
        """Try to advance amount lines 'down' in the map stream."""
        line = None
        while (amount > 0) and (line := input_io.readline()):
            amount -= 1
        return line

    trees = 0
    slope_right, slope_down = slope
    fline = input_io.readline().strip()
    assert fline[0] == "."
    columns = len(fline)
    current_column = 0
    while line := go_down(slope_down):
        line = line.strip()
        current_column += slope_right
        current_column %= columns
        trees += line[current_column] == "#"
    input_io.seek(0)
    return trees


def solve_task1(input_io: IO) -> int:
    """
    Solves task 1: number of trees for slope right 3 down 1.

    Parameters
    ----------
    input_io: IO
        Map stream.

    Return
    ------
    int
        Number of trees '#' in path from top to bottom.
    """
    return solve_task(input_io, (3, 1))


def solve_task2(input_io: IO) -> int:
    """
    Multiply number of trees under a set of predefined slopes.

    Parameters
    ----------
    input_io: IO
        Map stream.

    Returns
    -------
    int
        multiplication of number of trees.
    """
    return reduce(
        lambda a, b: a * b,
        (
            solve_task(input_io, slope)
            for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        ),
    )


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
        trees = solve_task1(file)
        print(f"Task 1: there are {trees} trees in the path.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        result = solve_task2(file)
        print(f"Task 2: multiplication result is {result}.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def test_solve_task():
    """Test solve_task with example."""
    map_stream = StringIO(
        """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""
    )
    trees = solve_task(map_stream, (3, 1))
    assert trees == 7


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        trees = solve_task1(file)
        assert trees == 230


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        result = solve_task2(file)
        assert result == 9533698720
