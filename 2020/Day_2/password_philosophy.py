#!/usr/bin/env python3
"""
Solves day 2 tasks of AoC 2020.

https://adventofcode.com/2020/day/2
"""

import argparse
import gzip
from io import StringIO
from os.path import dirname, realpath
from typing import List, Tuple, IO, Union, NewType, cast, Type
from dataclasses import dataclass
from pathlib import Path
from collections import Counter

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"


@dataclass(repr=True, frozen=True)
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


@dataclass(repr=True, frozen=True)
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
Password = NewType("Password", str)


def parse_passwords(
    input_io: IO, policy_type: Type[Policy]
) -> List[Tuple[Policy, Password]]:
    """
    Parse passwords file and returns list of policies and a passords.

    Parameters
    ----------
    input_io: IO
            Stream of passwords.

    policy_type: Type[Policy]
            Type of policy to be returned.

    Return
    ------
    List[Tuple[Policy, Password]]
        a list of tuples with policy and password for each entry in given file.
    """
    policies = []
    while line := input_io.readline():
        section = line.split(":")
        field = section[0].split(" ")
        lo_hi = field[0].strip().split("-")
        policy = policy_type(
            int(lo_hi[0].strip()), int(lo_hi[1].strip()), field[1].strip()
        )
        policies.append((policy, Password(section[1].strip())))
    return policies


def task1(entries: List[Tuple[PolicyTask1, Password]]) -> int:
    """
    Solves task 1.

    Parameters
    ----------
    entries: List[Tuple[PolicyTask1, str]]
        List of tuples of policy and passords.

    Return
    ------
    int
        Number of passwords conformant to task 1 policy.
    """
    num_valid = 0
    for policy, password in entries:
        counter = Counter(password)
        if policy.letter in counter:
            if (
                counter[policy.letter] >= policy.min_freq
                and counter[policy.letter] <= policy.max_freq
            ):
                num_valid += 1

    return num_valid


def task2(entries: List[Tuple[PolicyTask2, Password]]) -> int:
    """
    Solves task 2.

    Parameters
    ----------
    entries: List[Tuple[PolicyTask2, str]]
        List of tuples of policy and passords.

    Return
    ------
    int
        Number of passwords conformant to task 2 policy.
    """
    num_valid = 0
    for policy, password in entries:
        valid = False
        if (
            policy.first_pos <= len(password)
            and password[policy.first_pos - 1] == policy.letter
        ):
            valid = True

        if (
            policy.second_pos <= len(password)
            and password[policy.second_pos - 1] == policy.letter
        ):
            valid ^= True

        if valid:
            num_valid += 1
    return num_valid


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
        entries1 = cast(
            List[Tuple[PolicyTask1, Password]],
            parse_passwords(file, PolicyTask1),
        )
        valid_passwords = task1(entries1)
        print(f"Task 1: {valid_passwords} valid password in database")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        entries2 = cast(
            List[Tuple[PolicyTask2, Password]],
            parse_passwords(file, PolicyTask2),
        )
        valid_passwords = task2(entries2)
        print(f"Task 2: {valid_passwords} valid password in database")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def input_stream() -> IO:
    """Input stream fixture."""
    return StringIO(
        """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
    )


def test_parse_passwords():
    """Test parse_passwords."""
    pol_pass_list = cast(
        List[Tuple[PolicyTask1, Password]],
        parse_passwords(input_stream(), PolicyTask1),
    )

    assert len(pol_pass_list) == 3

    assert pol_pass_list[0][1] == "abcde"
    assert pol_pass_list[1][1] == "cdefg"
    assert pol_pass_list[2][1] == "ccccccccc"

    assert pol_pass_list[0][0] == PolicyTask1(1, 3, "a")
    assert pol_pass_list[1][0] == PolicyTask1(1, 3, "b")
    assert pol_pass_list[2][0] == PolicyTask1(2, 9, "c")


def test_task1_with_example_input():
    """Test task 1."""
    entries = cast(
        List[Tuple[PolicyTask1, Password]],
        parse_passwords(input_stream(), PolicyTask1),
    )
    valid_passwords = task1(entries)
    assert valid_passwords == 2


def test_taks1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        entries = cast(
            List[Tuple[PolicyTask1, Password]],
            parse_passwords(file, PolicyTask1),
        )
        valid_passwords = task1(entries)
        assert valid_passwords == 506


def test_task2_with_example_input():
    """Test task 2."""
    entries = cast(
        List[Tuple[PolicyTask2, Password]],
        parse_passwords(input_stream(), PolicyTask2),
    )
    valid_passwords = task2(entries)
    assert valid_passwords == 1


def test_taks2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        entries = cast(
            List[Tuple[PolicyTask2, Password]],
            parse_passwords(file, PolicyTask2),
        )
        valid_passwords = task2(entries)
        assert valid_passwords == 443
