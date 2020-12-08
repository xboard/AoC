#!/usr/bin/env python3
"""
Solves day X tasks of AoC 2020.

https://adventofcode.com/2020/day/X
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import IO, Iterator, Sequence, Tuple
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


@dataclass
class Instruction:
    """Program instruction representation."""

    oper: Operation
    value: int


def read_instructions(input_io: IO) -> Iterator[Instruction]:
    """Read instructions."""
    while line := input_io.readline():
        line = line.strip()
        yield Instruction(Operation.from_string(line[:3]), int(line[3:]))


def run_until_loop_or_end(program: Sequence[Instruction]) -> Tuple[int, bool]:
    """
    Interpret program until the end or finds a loop.

    Parameters
    ----------
    program: Sequence[Instruction]
        sequence of program instructions.

    Return
    ------
    Tuple[int, bool]
        int: last value of acc.
        bool: True if found loop.
              False if program was interpreted until the end.

    Raises
    ------
    Exception
        if no loop in found in given program.
        This is not suposed to happen with given AoC input.
    NotImplementedError
        if program has instruction not implemented.

    """
    # accumulator value
    acc = 0
    # instruction pointer
    inst_ptr = 0
    # record of previous instruction pointer values to find repeatition.
    ip_seen = set()
    looping = False

    while not looping and inst_ptr < len(program):
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

    return acc, looping


def task1(input_io: IO) -> int:
    """
    Solve task 1.

    Parameters
    ----------
    input_io: IO
        stream to program.

    Return
    ------
    int
        value of acc before looping.

    Raises
    ------
    Exception
        if no loop in found in given program.
        This is not suposed to happen with given AoC input.
    NotImplementedError
        if program has instruction not implemented.
    """
    program = tuple(read_instructions(input_io))
    result, looping = run_until_loop_or_end(program)
    if not looping:
        raise Exception("Invalid state: program has no loop")
    return result


def task2(input_io: IO) -> int:
    """
    Solve task 2.

    Parameters
    ----------
    input_io: IO
        stream to program.

    Return
    ------
    int
        value of acc after fix and program finishes.

    """
    program = tuple(read_instructions(input_io))
    for idx, instr in enumerate(program):

        modified_program = None

        if instr.oper in (Operation.NOP, Operation.JMP):
            modified_program = list(program)
            if instr.oper == Operation.NOP:
                modified_program[idx] = Instruction(Operation.JMP, instr.value)
            else:
                modified_program[idx] = Instruction(Operation.NOP, instr.value)

        if modified_program:
            result, looping = run_until_loop_or_end(modified_program)
            if not looping:
                return result

    raise Exception("Invalid state: program still loops.")


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
        acc = task2(file)
        print(f"Task 2: acc = {acc} after fix.")


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
    """Test function read_instructions with problem example."""
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
    assert next(instructions, None) is None


def test_task1_with_example_input():
    """Test task1 with input from problem example."""
    acc = task1(input_stream())
    assert acc == 5


def test_task2_with_example_input():
    """Test task2 with example problem example."""
    acc = task2(input_stream())
    assert acc == 8


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        acc = task1(file)
        assert acc == 1217


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        acc = task2(file)
        assert acc == 501
