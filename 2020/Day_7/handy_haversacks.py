#!/usr/bin/env python3
"""
Solves day 7 tasks of AoC 2020.

https://adventofcode.com/2020/day/7

The problem descriptions allow us to model the rules as a DAG (directed acyclic
graph) where a bag color is a node and directed edges point to all other color
bags that must be inside it.

References
----------
DAG: https://en.wikipedia.org/wiki/Directed_acyclic_graph
DFS: https://en.wikipedia.org/wiki/Depth-first_search
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import List, Tuple, Dict, IO, NewType, cast
from pathlib import Path
from functools import lru_cache

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"

BagColor = NewType("BagColor", str)
BagGraph = NewType("BagGraph", Dict[BagColor, List[Tuple[BagColor, int]]])


def generate_graph(input_io: IO) -> BagGraph:
    """
    Generate graph with Bag rules.

    Parameters
    ----------
    input_io: IO
        stream to all bag rules.

    Return
    ------
    BagGraph
        Graph representing bag rules.
    """
    dag = cast("BagGraph", dict())
    while line := input_io.readline():
        line = line.strip()
        section = [
            s.replace("bags", "").replace("bag", "").replace(".", "").strip()
            for s in line.split("contain")
        ]
        key = BagColor(section[0])
        dag[key] = list()
        if "no other" not in section[1]:
            bags = section[1].split(",")
            for bag in bags:
                dag[key].append(
                    (BagColor(" ".join(bag.split()[1:])), int(bag.split()[0]))
                )
    return dag


def task1(input_io: IO, bag_color: BagColor) -> int:
    """
    Solve task 1 using DFS and memoization.

    Parameters
    ----------
    input_io: IO
        stream to all bag rules.

    bag_color: BagColor
        bag color that must be included.

    Return
    ------
    int
        how many bag colors can eventually contain at least one bag_color.
    """
    dag = generate_graph(input_io)

    @lru_cache
    def dfs(node: BagColor) -> bool:
        if node == bag_color:
            return True
        for neigh, _ in dag[node]:
            found = dfs(neigh)
            if found:
                return True
        return False

    return sum(dfs(root) for root in dag if root != bag_color)


def task2(input_io: IO, bag_color: BagColor) -> int:
    """
    Solve task 2 using DFS.

    Parameters
    ----------
    input_io: IO
        stream to all bag rules.

    bag_color: BagColor
        bag color of most external bag.

    Return
    ------
    int
        how many indivigual bags are required inside a single bag_color.

    """
    dag = generate_graph(input_io)

    @lru_cache
    def dfs(node: BagColor) -> int:
        total = 0
        for neigh, qtd in dag[node]:
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
    dag = generate_graph(input_stream())

    assert len(dag.keys()) == 9
    assert len(dag["light red"]) == 2
    assert dag["light red"][0][1] == 1
    assert dag["light red"][1][1] == 2
    assert len(dag["faded blue"]) == 0
    assert len(dag["dotted black"]) == 0
    assert len(dag["bright white"]) == 1
    assert dag["bright white"][0][1] == 1


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
