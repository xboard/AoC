#!/usr/bin/env python3
"""
Solves problems for Day 1 of AoC 2020.

https://adventofcode.com/2020/day/1
"""

import argparse
import gzip
from io import StringIO
from os.path import dirname, realpath
from typing import List, IO
from pathlib import Path

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"


def read_expenses(input_io: IO) -> List[int]:
    """
    Read expenses in file and returns as list of integers.

    Parameters
    ----------
    input_io: IO
            Stream of expenses.

    Return
    ------
    list[int]
        a list of integers (expenses).
    """
    expenses = []
    while line := input_io.readline():
        expenses.append(int(line))
    return expenses


def task1(expenses: List[int], target: int = 2020) -> int:
    """
    Product of two numbers in expense list such that their sum equals target.

    O(N) solution.

    Parameters
    ----------
    expenses: List[int]
            List of expenses integers sorted in ascending order
    target: int, optional
            value that two expenses must add to be an answer (default is 2020)

    Return
    ------
    int
        the product of two expenses that sum to target.
    """
    left = 0
    right = len(expenses) - 1
    answer = -1
    while left < right:
        if expenses[left] + expenses[right] == target:
            answer = expenses[left] * expenses[right]
            break
        if expenses[left] + expenses[right] < target:
            left += 1
        else:
            right -= 1
    return answer


def task2(expenses: List[int], target: int = 2020) -> int:
    """
    Product of three numbers in expense list such that their sum equals target.

    Brute-force O(N^3) solution since N is very low (200 elements).
    Parameters
    ----------
    expenses: List[int]
            List of expenses integers sorted in ascending order
    target: int, optional
            value that two expenses must add to be an answer (default is 2020)

    Return
    ------
    int
        the product of three expenses that sum to target.
    """
    num_expenses = len(expenses)
    answer = -1
    for exp1 in range(num_expenses):
        for exp2 in range(exp1 + 1, num_expenses):
            for exp3 in range(exp2 + 1, num_expenses):
                if expenses[exp1] + expenses[exp2] + expenses[exp3] == target:
                    answer = expenses[exp1] * expenses[exp2] * expenses[exp3]
                    break
    return answer


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
    """Start script."""
    input_file = get_input_file()
    with gzip.open(input_file, "rt", encoding="ascii") as file:
        expenses = read_expenses(file)
        expenses.sort()
        answer = task1(expenses)
        print(f"Part 1 answer = {answer}")
        answer = task2(expenses)
        print(f"Part 2 answer = {answer}")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def input_stream() -> IO:
    """Input stream fixture."""
    return StringIO(
        """1721
979
366
299
675
1456"""
    )


def test_read_expenses():
    """Test parse_passwords."""
    expenses = read_expenses(input_stream())
    assert len(expenses) == 6
    assert sum(expenses) == 5496


def test_task1_with_example_input():
    """Test task 1."""
    expenses = read_expenses(input_stream())
    expenses.sort()
    answer = task1(expenses)
    assert answer == 514579


def test_taks1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        expenses = read_expenses(file)
        expenses.sort()
        answer = task1(expenses)
        assert answer == 440979


def test_task2_with_example_input():
    """Test task 2."""
    expenses = read_expenses(input_stream())
    expenses.sort()
    answer = task2(expenses)
    assert answer == 241861950


def test_taks2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        expenses = read_expenses(file)
        expenses.sort()
        answer = task2(expenses)
        assert answer == 82498112
