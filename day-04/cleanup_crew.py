"""Advent of Code 2022 - Day 4
"""
from __future__ import annotations
from attrs import frozen
from pathlib import Path


SAMPLE_INPUT = Path('sample-input.txt')
INPUT = Path('input.txt')


@frozen
class Range:
    """Integer range with endpoints included
    """

    min: int
    max: int

    def __attrs_post_init__(self):
        if self.min > self.max:
            raise ValueError(f'Expect min <=  max: ({self.min}, {self.max})')

    def __len__(self):
        """The number of integers included in this range"""
        return self.max - self.min + 1
    
    def contains(self, other) -> bool:
        """True if this range completely contains other, else False.
        Order matters! a.contains(b) and b.contains(a) may not give the same answer
        """
        return self.min <= other.min and self.max >= other.max

    def intersects(self, other) -> bool:
        """True if this range intersects other at all, else False"""
        return (
            (self.min <= other.max and self.max >= other.min) or
            (self.max >= other.min and self.min <= other.max)
        )           

    @classmethod
    def from_string(cls, txt) -> Range:
        """Parse a string like "min-max" to a new Range"""
        parts = txt.split('-')
        if len(parts) != 2: 
            raise ValueError(f'Could not parse {txt} as Range')
        return cls(int(parts[0]), int(parts[1]))


def parse_line(line) -> tuple[Range, Range]:
    """Parse a line like "min-max,min-max" to a pair of ranges
    """
    parts = line.split(',')
    if len(parts) != 2: 
        raise ValueError(f'Could not parse {line} as pair of Ranges')
    return tuple(Range.from_string(x) for x in parts)
        


def count_contains(pairs_path: Path):
    """Count the number of pairs in the input file in which one range 
    completely contains the other.
    """
    total = 0

    with open(pairs_path, 'r') as fp:
        for line in fp.readlines():
            r1, r2 = parse_line(line.strip())

            # check if larger range contains the smaller
            if len(r1) >= len(r2):
                total += r1.contains(r2)
            else:
                total += r2.contains(r1)
    return total


def count_intersects(pairs_path: Path):
    """Count the number of pairs in the input file in which one range
    intersects the other
    """
    total = 0

    with open(pairs_path, 'r') as fp:
        for line in fp.readlines():
            r1, r2 = parse_line(line.strip())
            total += r1.intersects(r2)
    return total


if __name__ == '__main__':
    
    print(f'[SAMPLE]: Pairs where one range contains the other {count_contains(SAMPLE_INPUT)}')
    print(f'[REAL  ]: Pairs where one range contains the other {count_contains(INPUT)}')
    print()
    print(f'[SAMPLE]: Pairs where ranges intersect {count_intersects(SAMPLE_INPUT)}')
    print(f'[REAL  ]: Pairs where ranges intersect {count_intersects(INPUT)}')
