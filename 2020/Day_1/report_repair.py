#!/usr/bin/env python3
"""
Solves problems for Day 1 of AoC 2020.

https://adventofcode.com/2020/day/1
"""

from typing import List
from pathlib import Path

INPUT_FILE_PATH = Path(".") / "input.txt"


def read_expenses(file_path: Path) -> List[int]:
    """
    Read expenses in file and returns as list of integers.

    Parameters
    ----------
    file_path: Path
            Path to expenses file

    Return
    ------
    list[int]
        a list of integers (expenses).
    """
    expenses = []
    with open(file_path, "r") as file:
        while line := file.readline():
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


def main() -> None:
    """Start script."""
    expenses = read_expenses(INPUT_FILE_PATH)
    expenses.sort()
    answer = task1(expenses)
    assert answer > 0
    print(f"Part 1 answer = {answer}")
    answer = task2(expenses)
    assert answer > 0
    print(f"Part 2 answer = {answer}")


if __name__ == "__main__":
    main()
