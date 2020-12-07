#!/usr/bin/env python3
"""
Solves day 4 tasks of AoC 2020.

https://adventofcode.com/2020/day/4
"""

import sys
import argparse
import gzip
from os.path import dirname, realpath
from io import StringIO
from typing import Callable, Dict, Iterator, List, IO
from pathlib import Path

INPUT_FILE_PATH = Path(dirname(realpath(__file__))) / "input.txt.gz"

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


def read_passports(input_io: IO) -> Iterator[Passport]:
    """
    Iterate over all passports in input_file.

    Parameters
    ----------
    input_path: Path
        Path to gziped input file with all passports to be validated.

    Return
    ------
    Iterator[Passport]
        Iterator to passports read (valid or invalid).
    """
    lines: List[str] = []
    while line := input_io.readline():
        line = line.strip()
        if len(line) == 0:
            yield read_passport(lines)
            lines.clear()
        else:
            lines.append(line)
    yield read_passport(lines)


def solve_task(input_io: IO, is_valid: Callable[[Passport], bool]) -> int:
    """
    Solve task 1 and 2: number of valid passports.

    Parameters
    ----------
    input_io: IO
        Stream of passports to be validated.

    is_valid: Callable[[Passport], bool]
        function to validate each passport.

    Return
    ------
    int
        Number of valid passports.
    """
    num_valid = 0
    for passport in read_passports(input_io):
        if is_valid(passport):
            num_valid += 1
    return num_valid


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
        num_valid_passports = solve_task(file, is_valid_task1)
        print(f"Task 1: there are {num_valid_passports} valid passports.")

    with gzip.open(input_file, "rt", encoding="ascii") as file:
        num_valid_passports = solve_task(file, is_valid_task2)
        print(f"Task 2: there are {num_valid_passports} valid passports.")


if __name__ == "__main__":
    main()

#######################
#    Tests section    #
#######################


def test_validate_passport_fields():
    """Test passport field validation."""
    assert is_valid_field("byr", "2002")
    assert not is_valid_field("byr", "2003")

    assert is_valid_field("hgt", "60in")
    assert is_valid_field("hgt", "190cm")
    assert not is_valid_field("hgt", "190in")
    assert not is_valid_field("hgt", "190")

    assert is_valid_field("hcl", "#123abc")
    assert not is_valid_field("hcl", "#123abz")
    assert not is_valid_field("hcl", "123abc")

    assert is_valid_field("ecl", "brn")
    assert not is_valid_field("ecl", "wat")

    assert is_valid_field("pid", "000000001")
    assert not is_valid_field("pid", "0123456789")


def test_invalid_passports_task1():
    """Test task 1 invalid passports."""
    passport_stream = StringIO(
        """iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""
    )
    passports = tuple(read_passports(passport_stream))
    assert len(passports) == 2
    assert all(not is_valid_task1(passport) for passport in passports)


def test_valid_passports_task1():
    """Test task 1 valid passports."""
    passport_stream = StringIO(
        """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277
"""
    )
    passports = tuple(read_passports(passport_stream))
    assert len(passports) == 2
    assert all(is_valid_task1(passport) for passport in passports)


def test_invalid_passports_task2():
    """Test task 2 invalid passports."""
    passport_stream = StringIO(
        """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""
    )
    passports = tuple(read_passports(passport_stream))
    assert len(passports) == 4
    assert all(not is_valid_task2(passport) for passport in passports)


def test_valid_passports_task2():
    """Test task2 valid passports."""
    passport_stream = StringIO(
        """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""
    )
    passports = tuple(read_passports(passport_stream))
    assert len(passports) == 4
    assert all(is_valid_task2(passport) for passport in passports)


def test_task1_with_input_file():
    """Test task1 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        num_valid_passports = solve_task(file, is_valid_task1)
        assert num_valid_passports == 216


def test_task2_with_input_file():
    """Test task2 with given input file (gziped)."""
    with gzip.open(INPUT_FILE_PATH, "rt", encoding="ascii") as file:
        num_valid_passports = solve_task(file, is_valid_task2)
        assert num_valid_passports == 150
