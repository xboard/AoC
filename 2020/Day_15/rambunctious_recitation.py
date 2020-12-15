#!/usr/bin/env python3
"""
Solves day 15 tasks of AoC 2020.

https://adventofcode.com/2020/day/15
"""

import argparse
from typing import Sequence, List
from collections import defaultdict

SEQUENCE = [14, 3, 1, 0, 9, 5]


def task(sequence: List[int], ith: int) -> int:
    """
    Solve task 1 or 2.

    Parameters
    ----------
    sequence: List[int]
        List with initial sequence.
    ith: int
        desired i-th number in sequence.

    Return
    ------
    int
        i-th number in sequence.
    """
    seen = defaultdict(list)
    for pos, num in enumerate(sequence):
        seen[num].append(pos)

    prev = sequence[-1]
    for pos in range(len(seen), ith):
        # print(f"seen[{prev}] = {seen[prev]}")
        if len(seen[prev]) < 2:
            curr = 0
        else:
            curr = seen[prev][-1] - seen[prev][-2]
        seen[curr].append(pos)
        prev = curr
    return prev


def get_input() -> List[int]:
    """
    Parse arguments passed to script.

    Return:
    Path
        path to gziped file for this problem.
    """
    parser = argparse.ArgumentParser()
    msg = "comma separated numbers, i.e '0,3,6'"
    parser.add_argument("sequence", help=msg)
    args = parser.parse_args()
    return list(map(int, args.sequence.split(",")))


def main() -> None:
    """Run script."""
    sequence = get_input()

    answer = task(sequence, 2020)
    print(f"Task 1: {answer}.")

    answer = task(sequence, 30000000)
    print(f"Task 2: {answer}.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def sample_seqs() -> Sequence[Sequence[int]]:
    """Sample seq from statement."""
    return ((1, 3, 2), (2, 1, 3), (1, 2, 3), (2, 3, 1), (3, 2, 1), (3, 1, 2))


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    assert task((0, 3, 6), 4) == 0
    assert task((0, 3, 6), 5) == 3
    assert task((0, 3, 6), 6) == 3
    assert task((0, 3, 6), 7) == 1
    assert task((0, 3, 6), 8) == 0
    assert task((0, 3, 6), 9) == 4
    assert task((0, 3, 6), 10) == 0

    seq = sample_seqs()

    ith = 2020
    assert task(seq[0], ith) == 1
    assert task(seq[1], ith) == 10
    assert task(seq[2], ith) == 27
    assert task(seq[3], ith) == 78
    assert task(seq[4], ith) == 438
    assert task(seq[5], ith) == 1836


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    val = task(SEQUENCE, 2020)
    assert val == 614


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    val = task(SEQUENCE, 30000000)
    assert val == 1065
