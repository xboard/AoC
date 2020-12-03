#!/usr/bin/env python3
"""
    Solves day 3 tasks of AoC 2020.
    https://adventofcode.com/2020/day/3
"""

import gzip
from typing import Tuple, Optional, IO
from pathlib import Path
from functools import reduce

INPUT_FILE_PATH = Path(".") / "input.txt.gz"


def answer_task(input_path: Path, slope: Tuple[int, int]) -> int:
    """
    Solves task 1: number of trees for slope right 3 down 1.

    Parameters
    ----------
    input_path: Path
        Path to gziped input file.

    slope: (slope_right: int, slope_down: int)
        Slope to use from top to botton.


    Returns
    -------
    int
        Number of trees '#' in path from top to bottom.
    """

    def go_down(file: IO, amount: int) -> Optional[str]:
        line = None
        while (amount > 0) and (line := file.readline()):
            amount -= 1
        return line

    trees = 0
    slope_right, slope_down = slope
    with gzip.open(input_path, "rt", encoding="ascii") as file:
        fline = file.readline().strip()
        assert fline[0] == "."
        columns = len(fline)
        current_column = 0
        while line := go_down(file, slope_down):
            line = line.strip()
            current_column += slope_right
            current_column %= columns
            trees += line[current_column] == "#"
    return trees


def answer_task1(input_path: Path) -> int:
    """
    Solves task 1: number of trees for slope right 3 down 1.

    Parameters
    ----------
    input_path: Path
        Path to gziped input file.

    Returns
    -------
    int
        Number of trees '#' in path from top to bottom.
    """

    return answer_task(input_path, (3, 1))


def answer_task2(input_path: Path) -> int:
    """
    Solves task 2: multiplication of number of trees under a set
    of predefined slopes.

    Parameters
    ----------
    input_path: Path
        Path to gziped input file.

    Returns
    -------
    int
        multiplication of number of trees.
    """

    return reduce(
        lambda a, b: a * b,
        [
            answer_task(input_path, slope)
            for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        ],
    )


def main() -> None:
    """ Starting function """

    trees = answer_task1(INPUT_FILE_PATH)
    assert trees == 230
    print(f"Task 1: there are {trees} trees in the path.")
    result = answer_task2(INPUT_FILE_PATH)
    assert result == 9533698720
    print(f"Task 2: multiplication result is {result}.")


if __name__ == "__main__":
    main()
