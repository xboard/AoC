#!/usr/bin/env python3
"""
Solves day 4 tasks of AoC 2020.

https://adventofcode.com/2020/day/4
"""

import sys
import gzip
from typing import Callable, Dict, List
from pathlib import Path

INPUT_FILE_PATH = Path(".") / "input.txt.gz"

Passport = Dict[str, str]


def read_passport(lines: List[str]) -> Passport:
    """
    Parse a list of lines to return a Passport.

    Parameters
    ----------
    lines: List[str]
        list of lines in file not separated by a empty line.

    Return
    ------
    Passport
        a passport (valid or invalid).
    """
    passport: Passport = dict()
    for line in lines:
        items = line.split()
        for item in items:
            key_value = item.split(":")
            passport[key_value[0]] = key_value[1]
    return passport


def is_valid_task1(passport: Passport) -> bool:
    """
    Validate passport for task1.

    Parameters
    ----------
    passport: Passport
        a passport to be validated by task 1 criteria

    Return
    ------
    bool
        True if passport is valid, False otherwise.
    """
    for field in ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"):
        if field not in passport:
            return False
    return True


def is_year_in_range(year: str, min_year: int, max_year: int) -> bool:
    """
    Return if year is a four digits year in between a range.

    Parameter
    ---------
    year: str
        a four digits year.
    min_year: int
        minimum year (inclusive) for year to be valid.
    max_year: int
        maximum year (inclusive) for year to be valid.

    Return
    ------
    bool
        True if pid is valid, False othewise.
    """
    if len(year) != 4:
        return False
    if not all((char.isdigit() for char in year)):
        return False
    return min_year <= int(year) <= max_year


def is_valid_byr(value: str) -> bool:
    """
    Return if value is a valid byr (birth year).

    Parameter
    ---------
    value: str
        a four digits byr.

    Return
    ------
    bool
        True if byr is valid, False othewise.
    """
    return is_year_in_range(value, 1920, 2002)


def is_valid_iyr(value: str) -> bool:
    """
    Return if value is a valid iyr (issue year).

    Parameter
    ---------
    value: str
        a four digits iyr.

    Return
    ------
    bool
        True if iyr is valid, False othewise.
    """
    return is_year_in_range(value, 2010, 2020)


def is_valid_eyr(value: str) -> bool:
    """
    Return if value is a valid eyr (expiration year).

    Parameter
    ---------
    value: str
        a four digits eyr.

    Return
    ------
    bool
        True if eyr is valid, False othewise.
    """
    return is_year_in_range(value, 2020, 2030)


def is_valid_hgt(value: str) -> bool:
    """
    Return if value is a valid hgt (height).

    Parameter
    ---------
    value: str
        a height in 'cm' or 'in'.

    Return
    ------
    bool
        True if height is valid, False othewise.
    """
    height, unit = value[:-2], value[-2:]
    if not all((char.isdigit() for char in height)):
        return False
    if unit == "in":
        return 59 <= int(height) <= 76
    if unit == "cm":
        return 150 <= int(height) <= 193

    return False


def is_valid_hcl(value: str) -> bool:
    """
    Return if value is a valid hcl (hair color).

    Parameter
    ---------
    value: str
        a hcl.

    Return
    ------
    bool
        True if hcl is valid, False othewise.
    """
    if value[0] != "#":
        return False
    return all((char.isdigit() or char in "abcdef" for char in value[1:]))


def is_valid_ecl(value: str) -> bool:
    """
    Return if value is a valid ecl (eye color).

    Parameter
    ---------
    value: str
        a ecl.

    Return
    ------
    bool
        True if ecl is valid, False othewise.
    """
    return any(
        (
            value == eye_color
            for eye_color in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
        )
    )


def is_valid_pid(value: str) -> bool:
    """
    Return if value is a valid pid (passport id).

    Parameter
    ---------
    value: str
        a pid.

    Return
    ------
    bool
        True if pid is valid, False othewise.
    """
    return len(value) == 9 and all((char.isdigit()) for char in value)


def is_valid_field(field: str, value: str) -> bool:
    """
    Return whether value in field is valid.

    Return
    ------
    bool
        True if value in field is valid, False othewise.
    """
    return getattr(sys.modules[__name__], f"is_valid_{field}")(value)


def is_valid_task2(passport: Passport) -> bool:
    """
    Return if a passport is valid by task 2 criteria.

    Parameters
    ----------
    passport: Passport
        passport to be validated.

    Return
    ------
    bool
        True if passport is valid, False othewise.
    """
    for field in ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"):
        if field not in passport:
            return False
        if not is_valid_field(field, passport[field]):
            return False
    return True


def read_passports(input_path: Path) -> List[Passport]:
    """
    Return list of all passports in input_file.

    Parameters
    ----------
    input_path: Path
        Path to gziped input file with all passports to be validated.

    Return
    ------
    List[Passport]
        List of passports read (valid or invalid).
    """
    passports = []
    with gzip.open(input_path, "rt", encoding="ascii") as file:
        lines: List[str] = []
        while line := file.readline():
            line = line.strip()
            if len(line) == 0:
                passports.append(read_passport(lines))
                lines.clear()
            else:
                lines.append(line)
        passports.append(read_passport(lines))
    return passports


def answer_task(input_path: Path, is_valid: Callable[[Passport], bool]) -> int:
    """
    Solves task 1 and 2: number of valid passports.

    Parameters
    ----------
    input_path: Path
        Path to gziped input file with all passports to be validated.

    is_valid: Callable[[Passport], bool]
        function to validate each passport.

    Return
    ------
    int
        Number of valid passports.
    """
    num_valid = 0
    passports = read_passports(input_path)
    for passport in passports:
        if is_valid(passport):
            num_valid += 1
    return num_valid


def main() -> None:
    """Run script."""
    num_valid_passports = answer_task(INPUT_FILE_PATH, is_valid_task1)
    assert num_valid_passports == 216
    print(f"Task 1: there are {num_valid_passports} valid passports.")

    num_valid_passports = answer_task(INPUT_FILE_PATH, is_valid_task2)
    assert num_valid_passports == 150
    print(f"Task 2: there are {num_valid_passports} valid passports.")


if __name__ == "__main__":
    main()
