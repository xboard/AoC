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
from enum import Enum
from dataclasses import dataclass

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"


class Operation(Enum):
    """Enumeration of CPU operations."""

    NOP = "nop"
    JMP = "jmp"
    ACC = "acc"

    @classmethod
    def from_string(cls, oper: str) -> "Operation":
        """Convert Op name to an Op object."""
        oper = oper.strip().upper()
        if oper in cls.__members__:
            return cls.__members__[oper]
        raise NameError(f"{oper} is not a valid {cls}")


@dataclass(frozen=True)
class Instruction:
    """Program instruction representation."""

    oper: Operation
    value: int


def read_instructions(input_io: IO) -> Iterator[Instruction]:
    """Read instructions."""
    while line := input_io.readline():
        line = line.strip()
        yield Instruction(Operation.from_string(line[:3]), int(line[3:]))


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
        .

    """
    # accumulator value
    acc = 0
    # instruction pointer
    inst_ptr = 0
    # record of previous instruction pointer values to find repeatition.
    ip_seen = set()
    looping = False
    # program.
    program = tuple(read_instructions(input_io))

    while not looping:
        if inst_ptr in ip_seen:
            looping = True
            continue
        instruction = program[inst_ptr]
        ip_seen.add(inst_ptr)
        if instruction.oper == Operation.NOP:
            inst_ptr += 1
        elif instruction.oper == Operation.ACC:
            acc += instruction.value
            inst_ptr += 1
        elif instruction.oper == Operation.JMP:
            inst_ptr += instruction.value
        else:
            raise NotImplementedError(
                f"Task 1 doesn't know how to handle op={instruction.oper}"
            )

    if not looping:
        raise Exception(f"Invalid state: program finished without looping. acc = {acc}")

    return acc


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
        acc = task1(file)
        print(f"Task 1: acc = {acc} before looping.")

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
        """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
    )


def test_read_instructions():
    instructions = read_instructions(input_stream())
    assert next(instructions) == Instruction(Operation.NOP, 0)
    assert next(instructions) == Instruction(Operation.ACC, 1)
    assert next(instructions) == Instruction(Operation.JMP, 4)
    assert next(instructions) == Instruction(Operation.ACC, 3)
    assert next(instructions) == Instruction(Operation.JMP, -3)
    assert next(instructions) == Instruction(Operation.ACC, -99)
    assert next(instructions) == Instruction(Operation.ACC, 1)
    assert next(instructions) == Instruction(Operation.JMP, -4)
    assert next(instructions) == Instruction(Operation.ACC, 6)
    assert next(instructions, None) == None


def test_task1_with_example_input():
    """Test task1."""
    acc = task1(input_stream())
    assert acc == 5


def test_task2_with_example_input():
    """Test task2."""
    acc = task2(input_stream())
    assert acc == 8


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        acc = task1(file)
        # assert val == 777


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        val = task2(file)
        # assert val == 777
