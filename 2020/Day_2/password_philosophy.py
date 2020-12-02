#!/usr/bin/env python3
"""
    Solves problems for Day 2 of AoC 2020.
    https://adventofcode.com/2020/day/2
"""

from dataclasses import dataclass
from typing import List, Tuple, Union, Type, cast, NewType
from pathlib import Path
from collections import Counter

INPUT_FILE_PATH = Path(".") / "input.txt"


@dataclass(repr=True)
class PolicyTask1:
    """
    Represents a password policy for Task 1.

    Attributes
    ----------
    min_freq: int

    max_freq: int

    letter: str
        letter
    """

    min_freq: int
    max_freq: int
    letter: str


@dataclass(repr=True)
class PolicyTask2:
    """
    Represents a password policy for Task 2.

    Attributes
    ----------
    first_pos: int
        First position to check for occurrence of letter in password

    second_pos: int
        Second position to check for occurrence of letter in password

    letter: str
        letter
    """

    first_pos: int
    second_pos: int
    letter: str


# Type Alias
Policy = Union[PolicyTask1, PolicyTask2]
Password = NewType('Password', str)


def parse_passwords(file_path: Path,
                    policy_type: Type[Policy])\
                         -> List[Tuple[Policy, Password]]:
    """
    Parses passwords files and returns list of tuples with a policy
    and a passord.

    Parameters
    ----------
    file_path: Path
            Path to passwords file

    policy_type: Type[Policy]
            Type of policy to be returned.

    Returns
    -------
    List[Tuple[Policy, Password]]
        a list of tuples with policy and password for each entry in given file.
    """

    policies = []
    with open(file_path, "r") as file:
        while line := file.readline():
            section = line.split(":")
            field = section[0].split(" ")
            minmax = field[0].strip().split("-")
            policy = policy_type(int(minmax[0].strip()),
                                 int(minmax[1].strip()),
                                 field[1].strip())
            policies.append((policy, Password(section[1].strip())))
    return policies


def answer_task1(entries: List[Tuple[PolicyTask1, Password]]) -> int:
    """
    Solves task 1.

    Parameters
    ----------
    entries: List[Tuple[PolicyTask1, str]]
        List of tuples of policy and passords.

    Returns
    -------
    int
        Number of passwords conformant to task 1 policy.
    """

    num_valid = 0
    for policy, password in entries:
        counter = Counter(password)
        if policy.letter in counter:
            if counter[policy.letter] >= policy.min_freq and\
               counter[policy.letter] <= policy.max_freq:
                num_valid += 1

    return num_valid


def answer_task2(entries: List[Tuple[PolicyTask2, Password]]) -> int:
    """
    Solves task 2.

    Parameters
    ----------
    entries: List[Tuple[PolicyTask2, str]]
        List of tuples of policy and passords.

    Returns
    -------
    int
        Number of passwords conformant to task 2 policy.
    """

    num_valid = 0
    for policy, password in entries:
        valid = False
        if policy.first_pos <= len(password) and\
           password[policy.first_pos - 1] == policy.letter:
            valid = True

        if policy.second_pos <= len(password) and\
           password[policy.second_pos - 1] == policy.letter:
            valid ^= True

        if valid:
            num_valid += 1
    return num_valid


def main() -> None:
    """ Starting function """

    entries1 = cast(List[Tuple[PolicyTask1, Password]],
                    parse_passwords(INPUT_FILE_PATH, PolicyTask1))
    valid_passwords = answer_task1(entries1)
    print(f'Task 1: there are {valid_passwords} valid password in database')

    entries2 = cast(List[Tuple[PolicyTask2, Password]],
                    parse_passwords(INPUT_FILE_PATH, PolicyTask2))
    valid_passwords = answer_task2(entries2)
    print(f'Task 2: there are {valid_passwords} valid password in database')


if __name__ == "__main__":
    main()
