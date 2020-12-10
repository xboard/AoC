#!/usr/bin/env python3
"""
Solves day X tasks of AoC 2020.

https://adventofcode.com/2020/day/X
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import IO, Iterator
from pathlib import Path
from collections import Counter
from operator import sub
from functools import lru_cache

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"


def read_numbers(input_io: IO) -> Iterator[int]:
    """
    Iterate adapter's joltage sequence in stream.

    Parameters
    ----------
    input_io: IO
        joltage stream.

    Return
    ------
    Iterator[int]
    """
    while line := input_io.readline():
        yield int(line.strip())


def task1(input_io: IO) -> int:
    """
    Solve task 1.

    Parameters
    ----------
    input_io: IO
        stream to all .

    Return
    ------
    int
        number of differentes of 1 times number of diferences of 3.

    """
    numbers = list(read_numbers(input_io))
    numbers.append(0)
    numbers.sort()
    counter = Counter(map(sub, numbers[1:], numbers[:-1]))
    return counter[1] * (counter[3] + 1)


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
        total number of distinct ways you can arrange the adapters.

    """
    numbers = list(read_numbers(input_io))
    numbers.sort()

    @lru_cache
    def dp_solve(prev_number: int, pos: int) -> int:
        if pos >= len(numbers):
            return 0
        if numbers[pos] - prev_number > 3:
            return 0
        if pos == len(numbers) - 1:
            return 1
        answer = (
            dp_solve(numbers[pos], pos + 1)
            + dp_solve(numbers[pos], pos + 2)
            + dp_solve(numbers[pos], pos + 3)
        )

        return answer

    return dp_solve(0, 0) + dp_solve(0, 1) + dp_solve(0, 2)


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
        answer = task1(file)
        print(f"Task 1: answer is {answer}.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        questions_solved = task2(file)
        print(f"Task 2: answer is {questions_solved}.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def input_stream_small() -> IO:
    """Input stream fixture small example."""
    return StringIO(
        """16
10
15
5
1
11
7
19
6
12
4"""
    )


def input_stream_large() -> IO:
    """Input stream fixture large example."""
    return StringIO(
        """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
    )


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    answer = task1(input_stream_small())
    assert answer == 35
    answer = task1(input_stream_large())
    assert answer == 220


def test_task2_with_example_input():
    """Test task2 with problem statement example."""
    answer = task2(input_stream_small())
    assert answer == 8
    answer = task2(input_stream_large())
    assert answer == 19208


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        answer = task1(file)
        assert answer == 2470


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        answer = task2(file)
        assert answer == 1973822685184
