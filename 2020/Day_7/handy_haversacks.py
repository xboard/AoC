#!/usr/bin/env python3
"""
Solves day 7 tasks of AoC 2020.

https://adventofcode.com/2020/day/7
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import List, Tuple, Dict, IO, NewType, cast
from pathlib import Path

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"

BagColor = NewType("BagColor", str)
BagGraph = NewType("BagGraph", Dict[BagColor, List[Tuple[BagColor, int]]])


def generate_graph(input_io: IO) -> BagGraph:
    """Generate graph with Bag rules."""
    graph = cast("BagGraph", dict())
    while line := input_io.readline():
        line = line.strip()
        section = [
            s.replace("bags", "").replace("bag", "").replace(".", "").strip()
            for s in line.split("contain")
        ]
        key = BagColor(section[0])
        graph[key] = list()
        if "no other" not in section[1]:
            bags = section[1].split(",")
            for bag in bags:
                graph[key].append(
                    (BagColor(" ".join(bag.split()[1:])), int(bag.split()[0]))
                )
    return graph


def task1(input_io: IO, bag_color: BagColor) -> int:
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
    graph = generate_graph(input_io)
    memo: Dict[BagColor, bool] = dict()

    def dfs(node: BagColor) -> bool:
        if node == bag_color:
            return True
        if node in memo:
            return memo[node]
        for neigh, _ in graph[node]:
            found = dfs(neigh)
            memo[neigh] = found
            if found:
                memo[node] = True
                return True
        memo[node] = False
        return False

    for root in graph:
        if root not in memo:
            dfs(root)

    return sum(memo[key] for key in memo) - 1


def task2(input_io: IO, bag_color: BagColor) -> int:
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
    graph = generate_graph(input_io)

    def dfs(node: BagColor) -> int:
        total = 0
        for neigh, qtd in graph[node]:
            total += qtd + qtd * dfs(neigh)
        return total

    return dfs(bag_color)


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
        bag_color = BagColor("shiny gold")
        qtd = task1(file, bag_color)
        print(f"Task 1: {qtd} bag colors can contain {bag_color}.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        bag_color = BagColor("shiny gold")
        qtd = task2(file, bag_color)
        print(f"Task 2: answer is {qtd}.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def input_stream() -> IO:
    """Input stream fixture."""
    return StringIO(
        """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
    )


def test_generate_graph():
    """Test generate_graph."""
    graph = generate_graph(input_stream())

    assert len(graph.keys()) == 9
    assert len(graph["light red"]) == 2
    assert graph["light red"][0][1] == 1
    assert graph["light red"][1][1] == 2
    assert len(graph["faded blue"]) == 0
    assert len(graph["dotted black"]) == 0
    assert len(graph["bright white"]) == 1
    assert graph["bright white"][0][1] == 1


def test_task1_with_example_input():
    """Test task1."""
    bag_color = BagColor("shiny gold")
    qtd = task1(input_stream(), bag_color)
    assert qtd == 4


def test_task2_with_example_input():
    """Test task2."""
    bag_color = BagColor("shiny gold")
    qtd = task2(input_stream(), bag_color)
    assert qtd == 32


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        bag_color = BagColor("shiny gold")
        qtd = task1(file, bag_color)
        assert qtd == 252


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        bag_color = BagColor("shiny gold")
        qtd = task2(file, bag_color)
        assert qtd == 35487
