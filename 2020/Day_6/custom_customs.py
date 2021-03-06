#!/usr/bin/env python3
"""
Solves day 6 tasks of AoC 2020.

https://adventofcode.com/2020/day/6
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import Sequence, List, Set, IO, Iterator, NewType, cast
from pathlib import Path

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"

# Defines type to represent customs answers from a group.
GroupCustoms = NewType("GroupCustoms", Sequence[str])


def read_groups_customs(input_io: IO) -> Iterator[GroupCustoms]:
    """
    Iterate group customs answers.

    input_io: IO
        stream to all customs answers from a group.

    Return
    ------
    Iterator[GroupCustoms]: Sequence[str]
        iterator to customs answers from group. Each string in the sequence
        corresponds to a group member customs answer.
    """
    group_lines: List[str] = []
    while line := cast("str", input_io.readline()):
        line = line.strip()
        if len(line) == 0:
            yield GroupCustoms(group_lines)
            group_lines.clear()
        else:
            group_lines.append(line)
    yield GroupCustoms(group_lines)


def task1(input_io: IO) -> int:
    """
    Solve task 1.

    Parameters
    ----------
    input_io: IO
        stream to all customs answers from a group.

    Return
    ------
    int
        sum of questions anyone answered "yes".

    """
    num_questions_solved = 0

    for group_custom in read_groups_customs(input_io):
        questions_set: Set[str] = set()
        for answer in group_custom:
            questions_set.update(answer)
        num_questions_solved += len(questions_set)

    return num_questions_solved


def task2(input_io: IO) -> int:
    """
    Solve task 2.

    Parameters
    ----------
    input_io: IO
        stream to all groups customs answers.

    Return
    ------
    int
        sum of questions every group members answered "yes".

    """
    num_questions_solved = 0

    for group_custom in read_groups_customs(input_io):
        questions_set = set(group_custom[0])
        for answer in group_custom[1:]:
            questions_set.intersection_update(answer)
        num_questions_solved += len(questions_set)

    return num_questions_solved


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
        questions_solved = task1(cast("IO", file))
        print(f"Task 1: {questions_solved} questions solved.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        questions_solved = task2(cast("IO", file))
        print(f"Task 2: answer is {questions_solved}.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def input_stream() -> IO:
    """Input stream fixture."""
    return StringIO(
        """abc

            a
            b
            c

            ab
            ac

            a
            a
            a
            a

            b"""
    )


def test_read_groups_customs():
    """Test read_group_customs."""
    i = 0
    for group_custom in read_groups_customs(input_stream()):
        assert group_custom is not None
        if i == 0:
            assert group_custom == ["abc"]
        elif i == 4:
            assert group_custom == ["b"]
        else:
            assert len(group_custom) > 1
        i += 1
    assert i == 5


def test_task1_with_example_input():
    """Test task1."""
    questions_solved = task1(input_stream())
    assert questions_solved == 11


def test_task2_with_example_input():
    """Test task2."""
    questions_solved = task2(input_stream())
    assert questions_solved == 6


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH) as file:
        questions_solved = task1(file)
        assert questions_solved == 6662


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH) as file:
        questions_solved = task2(file)
        assert questions_solved == 3382
