"""Advent of Code - Day ##
"""

from __future__ import annotations
from pathlib import Path
from attrs import frozen
from typing import Generator
from math import copysign


SAMPLE_INPUT_1 = Path('sample-input-1.txt')
SAMPLE_INPUT_2 = Path('sample-input-2.txt')
INPUT = Path('input.txt')


@frozen
class Position:
    row: int
    col: int

    def __add__(self, other):
        return Position(self.row + other.row, self.col + other.col)
    
    def __sub__(self, other):
        return Position(self.row - other.row, self.col - other.col)



def head_moves(input_file: Path) -> Generator[Position, None, None]:
    """Generator that yields a sequence of single-step moves parsed from 'input_file'
    """

    with open(input_file, 'r') as fp:
        for line in fp.readlines():

            direction, count = line.strip().split(' ')

            if direction == 'R':
                move = Position(0, 1)
            elif direction == 'L':
                move = Position(0, -1)
            elif direction == 'U':
                move = Position(-1, 0)
            elif direction == 'D':
                move = Position(1, 0)
            else:
                raise ValueError(f'Bad direction: {direction}')
            
            for _ in range(int(count)):
                yield move

def tail_move(head: Position, tail: position) -> Position:
    """Return the move that the tail will take given the position of the
    head it is attached to
    """
    delta = head - tail

    if (abs(delta.row) <= 1) and (abs(delta.col) <= 1):
        # touching, don't move tail
        return Position(0, 0)

    if delta.row == 0:
        # in same row 
        return Position(row=0, col=copysign(1, delta.col))

    if delta.col == 0:
        # in same col
        return Position(row=copysign(1, delta.row), col=0)

    # diagonal
    return Position(row=copysign(1, delta.row), col=copysign(1, delta.col))



def count_tail_positions(input_file: Path, rope_length: int):
    """Count all positions the tail of the rope occupies given the head moves in 
    'input_file' and a rope with 'rope_length' knots
    """
    rope = [Position(0, 0) for _ in range(rope_length)]

    tail_positions = set()

    for head_move in head_moves(input_file):
        rope[0] = rope[0] + head_move
        for idx in range(1, rope_length):
            rope[idx] = rope[idx] + tail_move(rope[idx-1], rope[idx])
        tail_positions.add(rope[-1])

    return len(tail_positions)
                


if __name__ == '__main__':

    print(f'[SAMPLE-1] tail positions: {count_tail_positions(SAMPLE_INPUT_1, 2)}')
    print(f'[REAL    ] tail positions: {count_tail_positions(INPUT, 2)}')
    print()
    print(f'[SAMPLE-1] tail positions: {count_tail_positions(SAMPLE_INPUT_1, 10)}')
    print(f'[SAMPLE-2] tail positions: {count_tail_positions(SAMPLE_INPUT_2, 10)}')
    print(f'[REAL    ] tail positions: {count_tail_positions(INPUT, 10)}')
