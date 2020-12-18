#!/usr/bin/env python3
"""
Solves day 18 tasks of AoC 2020.

https://adventofcode.com/2020/day/18
"""

import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import Sequence, Tuple, IO, Iterator
from pathlib import Path
from operator import add, mul
from enum import Enum, auto

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"

Token = str
Expression = Sequence[Token]


class Task(Enum):
    """Enumerate tasks."""

    task1 = auto()
    task2 = auto()


def tokenize(line: str) -> Sequence[Token]:
    """
    Tokenize string line with expression.

    Parameters
    ----------
    line: str
        single line with a mathematical expression.

    Return
    ------
    Sequence[Token]
        A sequence of token (integer, "+", "*","(" or ")") strings.
    """
    non_space = (char for char in line if char != " ")
    tokens = (char for char in non_space)
    return tuple(tokens)


def read_expressions(input_io: IO) -> Iterator[Expression]:
    """
    Iterate over expression's stream.

    Parameters
    ----------
    input_io: IO
        stream with all expressions.

    Return:
    -------
    Iterator[Expression]:
        iterator to all tokenized expressions in stream.
    """
    while line := input_io.readline():
        yield tokenize(line.strip())


def eval_par(expr: Expression, ptr: int, task: Task) -> Tuple[int, int]:
    """
    Evaluate a expression beginning with "(" at given position.

    Finds matching ")" in expression an evaluate expression in between.
    Parameters
    ----------
    expr: Expression
        A valid expression beginning with a left parenthesis "(" at ptr.
    ptr: position in expression where parenthesis expression
    to be evaluated starts.
    """
    counter = 0
    for idx, token in enumerate(expr[ptr:]):
        if token == "(":
            counter += 1
        if token == ")":
            counter -= 1
            if counter == 0:
                start = ptr + 1
                end = ptr + idx
                return evaluate(expr[start:end], task), end
    raise Exception("Malformed expression: parenthesis doesn't match!")


def evaluate(expr: Expression, task: Task) -> int:
    """Evaluate expression."""
    size = len(expr)
    ptr = 0
    result, val = None, None
    oper = None
    while ptr < size:
        if expr[ptr] == "(":
            val, ptr = eval_par(expr, ptr, task)
            if not result:
                result = val
                val = None
        elif expr[ptr] == "+":
            oper = add
        elif expr[ptr] == "*":
            oper = mul
            if task == Task.task2:
                nptr = ptr + 1
                val = evaluate(expr[nptr:], task)
                ptr = size
        else:
            val = int(expr[ptr])
            if not result:
                result = val
                val = None

        ptr += 1

        if result and oper and val:
            result = oper(result, val)
            val = None
            oper = None

    return result or 0


def task1(input_io: IO) -> int:
    """
    Solves task 1.

    Parameters
    ----------
    input_io: IO
        stream to all expressions.

    Return
    ------
    int
        Sum of expressions evaluations.

    """
    expressions = read_expressions(input_io)
    return sum(evaluate(expr, Task.task1) for expr in expressions)


def task2(input_io: IO) -> int:
    """
    Solves task 2.

    Parameters
    ----------
    input_io: IO
        stream to all .

    Return
    ------
    int
        Sum of expressions evalutaions.

    """
    expressions = read_expressions(input_io)
    return sum(evaluate(expr, Task.task2) for expr in expressions)


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
        """1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
((6))"""
    )


def test_read_expressions():
    """Test read_expressions function."""
    expressions = tuple(read_expressions(input_stream()))
    assert len(expressions) == 7
    assert len(expressions[0]) == 11
    assert len(expressions[5]) == 27


def test_eval_task1():
    """Test eval with task1."""
    expressions = read_expressions(input_stream())

    expression = next(expressions)
    assert evaluate(expression, Task.task1) == 71

    expression = next(expressions)
    assert evaluate(expression, Task.task1) == 51

    expression = next(expressions)
    assert evaluate(expression, Task.task1) == 26

    expression = next(expressions)
    assert evaluate(expression, Task.task1) == 437

    expression = next(expressions)
    assert evaluate(expression, Task.task1) == 12240

    expression = next(expressions)
    assert evaluate(expression, Task.task1) == 13632

    expression = next(expressions)
    assert evaluate(expression, Task.task1) == 6

    assert next(expressions, None) is None


def test_task1_with_example_input():
    """Test task1 with problem statement example."""
    answer = task1(input_stream())
    assert answer == 26463


def test_eval_task2():
    """Test eval with task2."""
    expressions = read_expressions(input_stream())

    expression = next(expressions)
    assert evaluate(expression, Task.task2) == 231

    expression = next(expressions)
    assert evaluate(expression, Task.task2) == 51

    expression = next(expressions)
    assert evaluate(expression, Task.task2) == 46

    expression = next(expressions)
    assert evaluate(expression, Task.task2) == 1445

    expression = next(expressions)
    assert evaluate(expression, Task.task2) == 669060

    expression = next(expressions)
    assert evaluate(expression, Task.task2) == 23340

    expression = next(expressions)
    assert evaluate(expression, Task.task2) == 6

    assert next(expressions, None) is None


def test_task2_with_example_input():
    """Test task2 with problem statement example."""
    answer = task2(input_stream())
    assert answer == 694179


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        answer = task1(file)
        assert answer == 98621258158412


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        answer = task2(file)
        assert answer == 241216538527890
