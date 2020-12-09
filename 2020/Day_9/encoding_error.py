#!/usr/bin/env python3
"""
Solves day 9 tasks of AoC 2020.

https://adventofcode.com/2020/day/9
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import Sequence, List, Set, IO, Iterator, NewType, cast
from pathlib import Path

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"


def read_numbers(input_io: IO) -> Iterator[int]:
    while line := input_io.readline():
        yield (int(line.strip()))


def task1(input_io: IO, preamble: int) -> int:
    """
    Solve task 1.

    O(n) time and additional O(n) space.

    Parameters
    ----------
    input_io: IO
        stream of XMAS numbers.

    preamble: int
        size of preamble sequence.

    Return
    ------
    int
        number in stream not having the XMAS property.
    """
    seen_at = dict()  # dictinario[number] = position.
    numbers = tuple(read_numbers(input_io))
    answer = None
    for pos, number in enumerate(numbers):
        seen_at[number] = pos
        if pos >= preamble:
            found = False
            idx = pos - 1
            while idx >= pos - preamble and not found:
                looking_for = number - numbers[idx]
                if (looking_for in seen_at) and (
                    pos > seen_at[looking_for] >= pos - preamble
                ):
                    found = True
                    break
                idx -= 1
            if not found:
                answer = number
                break
    if answer is None:
        raise Exception("No answer found!")

    return answer


def task2(input_io: IO) -> int:
    """
    Solve task 2.

    Parameters
    ----------
    input_io: IO
        stream to all .

    Return
    ------
    int
        .

    """
    pass


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
        wrong_number = task1(file, 25)
        print(f"Task 1: wrong number is {wrong_number}.")

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
        """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
    )


def test_read_numbers():
    """Test function read_numbers."""
    number_gen = read_numbers(input_stream())
    assert next(number_gen) == 35
    assert next(number_gen) == 20

    for i in range(17):
        assert next(number_gen, None) is not None

    assert next(number_gen) == 576
    assert next(number_gen, None) is None


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    wrong_number = task1(input_stream(), 5)
    assert wrong_number == 127


def test_task2_with_example_input():
    """Test task2 with problem statement example."""
    questions_solved = task2(input_stream())
    assert questions_solved == 6


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        wrong_number = task1(file, 25)
        assert wrong_number == 32321523


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        val = task2(file)
        assert val == 777
