#!/usr/bin/env python3
"""
Solves day 14 tasks of AoC 2020.

https://adventofcode.com/2020/day/14
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import Sequence, List, Dict, IO, Iterator, NewType, cast
from pathlib import Path
from dataclasses import dataclass
from re import findall

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"

@dataclass
class MemOp:
    address: int
    unmasked_value: int


@dataclass
class Initialization:
    off_positions: List[int]
    on_positions: List[int] 
    mem_ops: List[MemOp]

    def apply_masks(self, value: int) -> int:
        masked_value = value
        for pos in self.on_positions:
            masked_value |= (1 << pos)
        for pos in self.off_positions:
            masked_value &= ~(1 << pos)
        return masked_value    


def read_initialization(input_io: IO) -> Iterator[Initialization]:
    def parse_mask(line: str):
        sections = line.split()
        answer = [[],[]]
        for pos, bit in enumerate(reversed(sections[2])):
            if bit != "X":
                answer[int(bit)].append(pos)
        return tuple(answer)

    def parse_mem(line: str):
        address = int(findall(r"\[(\d+)\]", line)[0])
        uv = int(findall(r"\d+$", line)[0])
        return MemOp(address, uv)

    line = input_io.readline().strip()
    initialization = Initialization(*parse_mask(line), list())
    while line := input_io.readline():
        line = line.strip()
        if "mask" in line:
            yield initialization
            initialization = Initialization(*parse_mask(line), list())
        else:
            initialization.mem_ops.append(parse_mem(line))
    yield initialization


def apply_maks(value: int, on_pos: List[int], off_pos: List[int]) -> int:
    masked_value = value
    for pos in on_pos:
        masked_value |= (1 << pos)
    for pos in off_pos:
        masked_value &= ~(1 << pos)
    return masked_value

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
    mem_value_map: Dict[int, int] = dict()
    for i12n in read_initialization(input_io):
        for mem_op in i12n.mem_ops:
            mem_value_map[mem_op.address] = i12n.apply_masks(mem_op.unmasked_value)
    
    return sum(mem_value_map.values())



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
        answer = task1(file)
        print(f"Task 1: the sum of all values left in memory is {answer}.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        answer = task2(file)
        print(f"Task 2: answer is {answer}.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def input_stream() -> IO:
    """Input stream fixture."""
    return StringIO(
        """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
    )


def test_read_initialization():
    """Test read_initialization function."""
    i12n: Initialization = next(read_initialization(input_stream()))
    assert i12n.on_positions == [6]
    assert i12n.off_positions == [1]
    assert len(i12n.mem_ops) == 3
    assert i12n.mem_ops[0] == MemOp(8, 11)
    assert i12n.mem_ops[1] == MemOp(7, 101)
    assert i12n.mem_ops[2] == MemOp(8, 0)
    assert i12n.apply_masks(11) == 73
    assert i12n.apply_masks(101) == 101
    assert i12n.apply_masks(0) == 64 


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    answer = task1(input_stream())
    assert answer == 165


# def test_task2_with_example_input():
#     """Test task2 with problem statement example."""
#     questions_solved = task2(input_stream())
#     assert questions_solved == 6


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        answer = task1(file)
        assert answer == 12610010960049


# def test_task2_with_input_file():
#     """Test task2 with given input file (gziped)."""
#     with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
#         val = task2(file)
#         assert val == 777



def mask_fn(mask: str):
    def get_masked_value(value:int)->int:
        newvalue = 0
        for i, bit in enumerate(reversed(mask)):
            vbit = value & (2**i)
            if bit == "X":
                newvalue += vbit
            elif bit == "1":
                newvalue += 2**i
            elif bit == "0":
                pass
            else:
                assert False
        return newvalue
    return get_masked_value
