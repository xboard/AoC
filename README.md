# AoC
[![CI](https://github.com/xboard/AoC/workflows/CI/badge.svg)](https://github.com/xboard/AoC/actions?query=workflow%3ACI)
![Python](https://img.shields.io/badge/Python%203.8-3776AB?logo=Python&logoColor=white&style=flat)

[Advent of Code](https://adventofcode.com/) solutions in Python 3.

## Pre-requisites

- python 3.8+
- pytest 6.1+


## To run


Go to challenge year/day directory and type `python3 <script_name>.py input.txt.gz`, for instance to run solution 
for day 8 of AoC 2020:
```
cd 2020/Day_8
python3 handheld_halting.py input.txt.gz
```

You can pass a path to your own input files but you must gzip it first:
```
python3 handheld_halting.py /tmp/another_input_file.txt.gz
```

### Design

Every problem solution is designed to be easy to understand, unit testable, self-contained (including unit tests), 
idiomatic and to (ab)use type annotations.


### Unit tests

Install `pytest`:

```
pip install -r requirements.txt 
```

To run all unit tests for all problems:
```
pytest **/*.py 
```

To run unit tests for a specific problem:
```
pytest <path_to_problem>/*.py
```
