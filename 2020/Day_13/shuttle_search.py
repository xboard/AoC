#!/usr/bin/env python3
"""
Solves day 13 tasks of AoC 2020.

https://adventofcode.com/2020/day/13
"""

import argparse
import gzip
import math
from os.path import dirname, realpath
from io import StringIO
from typing import List, Tuple, IO
from pathlib import Path
from dataclasses import dataclass

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"


@dataclass
class Notes:
    """Notes class."""

    earliest_timestamp: int
    buses: List[int]


def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Modular binary exponentiation.

    https://cp-algorithms.com/algebra/binary-exp.html

    Parameters
    ----------
    base: int
    exp: int
        exponent
    mod: int
        module

    Return
    ------
    int
        (base ** exp) % mod
    """
    resp = 1
    while exp:
        if exp % 2 == 1:
            resp = (base * resp) % mod
            exp -= 1
        base = (base * base) % mod
        exp //= 2
    return resp


def mod_inverse(num: int, mod: int) -> int:
    """
    Calculate module multiplicative inverse.

    https://cp-algorithms.com/algebra/module-inverse.html

    Parameters
    ----------
    num: int
    mod: int
        prime as module

    Return
    ------
    int
        module multiplicative inverse num_inv s.t  (num_inv * num) % mod == 1
    """
    return mod_pow(num, mod - 2, mod)


def read_notes(input_io: IO) -> Notes:
    """
    Read notes.

    Parameters
    ----------
    input_io: IO
        stream to notes.

    Return
    ------
    Notes
        a Notes object read from stream.
    """
    timestamp = int(input_io.readline().strip())
    line2 = input_io.readline().strip()
    buses = list(map(lambda id: 0 if id == "x" else int(id), line2.split(",")))
    return Notes(timestamp, buses)


def task1(input_io: IO) -> int:
    """
    Solve task 1.

    Parameters
    ----------
    input_io: IO
        stream to notes.

    Return
    ------
    int
        earliest bus id multiplied by the waiting time.

    """
    notes = read_notes(input_io)
    min_wait = math.inf
    answer = 0
    for bus in notes.buses:
        if bus == 0:
            continue
        wait = -(notes.earliest_timestamp % -bus)
        if wait < min_wait:
            min_wait = wait
            answer = bus * wait
    return answer


def crt(equations: List[Tuple[int, int]]) -> int:
    """
    Chinese remainder theorem: Garner's algorithm.

    https://cp-algorithms.com/algebra/chinese-remainder-theorem.html#toc-tgt-2

    Parameter
    ---------
    equations: List[Tuple[int, int]]
        List os pair (p_i, a_i) where p_i is the i-th prime and a_i the i-th
        remainder.

    Return:
    -------
        int
            solution x of CRT equation system (x % p_i = a_i ).

    """
    ans = 0
    num_equations = len(equations)
    mult_primes = 1
    for i in range(num_equations):
        mult_primes *= equations[i][0]

    for i in range(num_equations):
        partial = 1
        for j in range(i):
            partial *= equations[j][0]
            partial *= mod_inverse(equations[j][0], equations[i][0])
            partial %= mult_primes

        ans += (partial * (equations[i][1] + mult_primes - ans)) % mult_primes
        ans %= mult_primes

    return ans


def task2(input_io: IO) -> int:
    """
    Solve task 2.

    It's an application of the Chinese Remainder Theorem.
    https://en.wikipedia.org/wiki/Chinese_remainder_theorem

    Parameters
    ----------
    input_io: IO
        stream to all .

    Return
    ------
    int
        earliest timestamp such that all of the listed bus IDs
        depart at offsets matching their positions in the list.

    """
    notes = read_notes(input_io)
    equations = []
    for idx, bus in enumerate(notes.buses):
        if bus == 0:
            continue
        equations.append((bus, (bus - idx + bus) % bus))
    return crt(equations)


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
        questions_solved = task1(file)
        print(f"Task 1: {questions_solved} questions solved.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        questions_solved = task2(file)
        print(f"Task 2: answer is {questions_solved}.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def input_stream() -> IO:
    """Input stream fixture."""
    return StringIO(
        """939
7,13,x,x,59,x,31,19"""
    )


def test_read_notes():
    """Test read_notes function."""
    notes = read_notes(input_stream())
    assert notes.earliest_timestamp == 939
    assert len(notes.buses) == 8
    assert sum(notes.buses) == 129


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    answer = task1(input_stream())
    assert answer == 295


def test_task2_with_example_input():
    """Test task2 with problem statement example."""
    answer = task2(input_stream())
    assert answer == 1068781


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        answer = task1(file)
        assert answer == 4207


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        val = task2(file)
        assert val == 725850285300475
