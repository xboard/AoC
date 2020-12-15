#!/usr/bin/env python3
"""
Solves day 14 tasks of AoC 2020.

https://adventofcode.com/2020/day/14
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import List, Tuple, Set, Dict, IO, Iterator, cast
from pathlib import Path
from dataclasses import dataclass
from re import findall
from collections import deque

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"


@dataclass
class MemOp:
    """
    Memory operation.

    mem[address] = unmasked_value
    """

    address: int
    unmasked_value: int


@dataclass
class Initialization:
    """Represent a boot initialization."""

    off_positions: Set[int]
    on_positions: Set[int]
    mem_ops: List[MemOp]

    def mask_value(self, value: int) -> int:
        """Mask a memory value - Task 1."""
        masked_value = value
        for pos in self.on_positions:
            masked_value |= 1 << pos
        for pos in self.off_positions:
            masked_value &= ~(1 << pos)
        return masked_value

    def mask_address(self, addr: int) -> str:
        """Mask a memory address - Task 2."""
        masked_addr = f"{addr:b}"[::-1]
        masked_addr += "0" * (36 - len(masked_addr))
        for pos in range(36):
            inc_pos = pos + 1
            if pos not in self.on_positions and pos not in self.off_positions:
                masked_addr = masked_addr[:pos] + "X" + masked_addr[inc_pos:]
            elif pos in self.on_positions:
                masked_addr = masked_addr[:pos] + "1" + masked_addr[inc_pos:]
        return masked_addr[::-1]


def read_initialization(input_io: IO) -> Iterator[Initialization]:
    """Read initialization stream."""

    def parse_mask(line: str) -> Tuple[Set[int], Set[int]]:
        sections = line.split()
        answer: List[Set[int]] = [set(), set()]
        for pos, bit in enumerate(reversed(sections[2])):
            if bit != "X":
                answer[int(bit)].add(pos)
        return cast("Tuple[Set[int], Set[int]]", tuple(answer))

    def parse_mem(line: str):
        address = int(findall(r"\[(\d+)\]", line)[0])
        unmasked_value = int(findall(r"\d+$", line)[0])
        return MemOp(address, unmasked_value)

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


def addresses_list(addr: str) -> List[int]:
    """Return list of address from a masked address."""
    updated = True
    addresses = []
    to_gen = deque([addr])
    while to_gen:
        addr = to_gen.popleft()
        updated = False
        for pos, _ in enumerate(addr):
            inc_pos = pos + 1
            if addr[pos] == "X":
                new_addr0 = addr[:pos] + "0" + addr[inc_pos:]
                new_addr1 = addr[:pos] + "1" + addr[inc_pos:]
                to_gen.append(new_addr0)
                to_gen.append(new_addr1)
                updated = True
                break
        if not updated:
            addresses.append(addr)

    return [int(address, 2) for address in addresses]


def task1(input_io: IO) -> int:
    """
    Solve task 1.

    Parameters
    ----------
    input_io: IO
        stream to initializations.

    Return
    ------
    int
        sum of initialized memory values.

    """
    mem_value_map: Dict[int, int] = dict()

    for i12n in read_initialization(input_io):
        for mem_op in i12n.mem_ops:
            masked_value = i12n.mask_value(mem_op.unmasked_value)
            mem_value_map[mem_op.address] = masked_value

    return sum(mem_value_map.values())


def task2(input_io: IO) -> int:
    """
    Solve task 2.

    Parameters
    ----------
    input_io: IO
        stream to initializations.

    Return
    ------
    int
        sum of initialized memory values..

    """
    mem_value_map: Dict[int, int] = dict()

    for i12n in read_initialization(input_io):
        for mem_op in i12n.mem_ops:
            masked_address = i12n.mask_address(mem_op.address)
            for addr in addresses_list(masked_address):
                mem_value_map[addr] = mem_op.unmasked_value

    return sum(mem_value_map.values())


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
        print(f"Task 2: the sum of all values left in memory is {answer}.")


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


def input_stream2() -> IO:
    """Input stream fixture."""
    return StringIO(
        """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
    )


def test_read_initialization():
    """Test read_initialization function."""
    i12n: Initialization = next(read_initialization(input_stream()))
    assert i12n.on_positions == {6}
    assert i12n.off_positions == {1}
    assert len(i12n.mem_ops) == 3
    assert i12n.mem_ops[0] == MemOp(8, 11)
    assert i12n.mem_ops[1] == MemOp(7, 101)
    assert i12n.mem_ops[2] == MemOp(8, 0)
    assert i12n.mask_value(11) == 73
    assert i12n.mask_value(101) == 101
    assert i12n.mask_value(0) == 64


def test_mask_address():
    """Test mask_address function."""
    init = read_initialization(input_stream2())
    i12n: Initialization = next(init)
    assert i12n.on_positions == {1, 4}
    assert len(i12n.off_positions) == 32
    assert i12n.mask_address(42) == "000000000000000000000000000000X1101X"

    i12n: Initialization = next(init)
    assert i12n.on_positions == set()
    assert len(i12n.off_positions) == 33
    assert i12n.mask_address(26) == "00000000000000000000000000000001X0XX"


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    answer = task1(input_stream())
    assert answer == 165


def test_task2_with_example_input():
    """Test task2 with problem statement example."""
    answer = task2(input_stream2())
    assert answer == 208


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        answer = task1(file)
        assert answer == 12610010960049


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        answer = task2(file)
        assert answer == 3608464522781
