#!/usr/bin/env python3
"""
Solves day 16 tasks of AoC 2020.

https://adventofcode.com/2020/day/16
"""

import argparse
import gzip
import re
from os.path import dirname, realpath
from io import StringIO
from typing import Set, Dict, List, Tuple, IO
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"

RULE_RGEXP = r"(\w+\s*\w*):\s([\d-]+)\sor\s([\d-]+)"


@dataclass
class Rule:
    """Field rule class."""

    min_val: int
    max_val: int


@dataclass
class Notes:
    """Notes class."""

    rules: Dict[str, List[Rule]]
    ticket: List[int]
    nearby: List[List[int]]


def read_notes(input_io: IO) -> Notes:
    """Read notes from stream."""
    rules = defaultdict(list)
    ticket = []
    nearby = []
    while line := input_io.readline():
        line = line.strip()
        if match := re.findall(RULE_RGEXP, line):
            match = match[0]
            for rule_str in match[1:]:
                min_val = int(rule_str.split("-")[0])
                max_val = int(rule_str.split("-")[1])
                rules[match[0]].append(Rule(min_val, max_val))
        elif match := re.findall("^your ticket:", line):
            line = input_io.readline().strip()
            ticket = [int(val) for val in line.split(",")]
        elif match := re.findall("^nearby tickets:", line):
            while line := input_io.readline():
                line = line.strip()
                nearby.append([int(val) for val in line.split(",")])
    return Notes(rules, ticket, nearby)


def get_invalid_tickets(notes: Notes) -> Tuple[List[int], Set[int]]:
    """Get list of invalid tickets in notes."""
    invalid_values = []
    invalid_tickets = []
    for idx, ticket in enumerate(notes.nearby):
        for field_value in ticket:
            is_valid = False
            for rules in notes.rules.values():
                rule0, rule1 = rules
                if (
                    rule0.min_val <= field_value <= rule0.max_val
                    or rule1.min_val <= field_value <= rule1.max_val
                ):
                    is_valid = True
                    break
            if not is_valid:
                invalid_values.append(field_value)
                invalid_tickets.append(idx)
    return invalid_values, set(invalid_tickets)


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
        sum of all invalid fields in nearby tickets.

    """
    notes = read_notes(input_io)
    invalid, _ = get_invalid_tickets(notes)
    return sum(invalid)


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
        multiplication of all departure values in my ticket.

    """
    notes = read_notes(input_io)

    _, invalid_tickets = get_invalid_tickets(notes)

    valid_tickets = get_valid_tickets(notes, invalid_tickets)

    column_name, name_column = get_candidate_columns(notes, valid_tickets)

    assert len(name_column.items()) == 20

    propagate_constraints(column_name, name_column)

    answer = 1
    for col, names in column_name.items():
        name = names[0]
        if not name.startswith("departure"):
            continue
        answer *= notes.ticket[col]
    return answer


def propagate_constraints(
    col_name: Dict[int, List[str]], name_col: Dict[str, List[int]]
):
    """Propagate constraints."""
    ok_columns: Set[int] = set()
    while len(ok_columns) < 20:
        for col, names in col_name.items():
            if col in ok_columns:
                continue
            if len(names) == 1:
                # if found unique field for a column,
                # remove field from other columns (propagate constraint).
                name = names[0]
                ok_columns.add(col)
                for wcol in name_col[name]:
                    if wcol == col:
                        continue
                    col_name[wcol].remove(name)
                name_col[name] = [col]


def get_candidate_columns(notes: Notes, valid_tickets: List[List[int]]):
    """Get candidate columns."""
    column_name = defaultdict(list)
    name_column = defaultdict(list)
    for name, rules in notes.rules.items():
        rul0, rul1 = rules
        for col in range(len(notes.ticket)):
            all_valid = True
            for row, _ in enumerate(valid_tickets):
                val = valid_tickets[row][col]
                if (
                    not rul0.min_val <= val <= rul0.max_val
                    and not rul1.min_val <= val <= rul1.max_val
                ):
                    all_valid = False
                    break
            if all_valid:
                column_name[col].append(name)
                name_column[name].append(col)
    return column_name, name_column


def get_valid_tickets(notes: Notes, invalid: Set[int]) -> List[List[int]]:
    """Get valid tickets in Notes."""
    valid_tickets = []
    for idx, tickets in enumerate(notes.nearby):
        if idx not in invalid:
            valid_tickets.append(tickets)
    return valid_tickets


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
        """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    )


def test_read_notes():
    """Test read_notes."""
    notes = read_notes(input_stream())
    assert notes is not None
    assert len(notes.rules) == 3
    assert len(notes.ticket) == 3
    assert len(notes.nearby) == 4
    assert notes.rules["class"] == [Rule(1, 3), Rule(5, 7)]
    assert notes.rules["seat"] == [Rule(13, 40), Rule(45, 50)]
    assert notes.ticket == [7, 1, 14]
    assert notes.nearby[0] == [7, 3, 47]
    assert notes.nearby[1] == [40, 4, 50]
    assert notes.nearby[2] == [55, 2, 20]
    assert notes.nearby[3] == [38, 6, 12]


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    valid = task1(input_stream())
    assert valid == 71


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        valid = task1(file)
        assert valid == 32835


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        valid = task2(file)
        assert valid == 514662805187
