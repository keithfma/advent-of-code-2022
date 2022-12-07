"""Advent of Code - Day 6
"""

from pathlib import Path


SAMPLE_INPUT_1 = Path('sample-input-1.txt')
SAMPLE_INPUT_2 = Path('sample-input-2.txt')
SAMPLE_INPUT_3 = Path('sample-input-3.txt')
SAMPLE_INPUT_4 = Path('sample-input-4.txt')
INPUT = Path('input.txt')


def start_idx(input_file: Path, width: int) -> int:
    """Find sequence of 'width' unique character and return integer index
    of the character after the end of that sequence
    """
    with open(input_file, 'r') as fp:
        txt = fp.read().strip()

    for idx in range(len(txt)):
        window = txt[idx:idx+width]
        if len(window) != width:
            raise ValueError(f'No sequence of width {width} found!')
        if len(set(window)) == width:
            return idx + width

    raise ValueError(f'No sequence of width {width} found!')



if __name__ == '__main__':

    print(f'[SAMPLE-1] Packet start at: {start_idx(SAMPLE_INPUT_1, 4)}')
    print(f'[SAMPLE-2] Packet start at: {start_idx(SAMPLE_INPUT_2, 4)}')
    print(f'[SAMPLE-3] Packet start at: {start_idx(SAMPLE_INPUT_3, 4)}')
    print(f'[SAMPLE-4] Packet start at: {start_idx(SAMPLE_INPUT_4, 4)}')
    print(f'[REAL    ] Packet start at: {start_idx(INPUT, 4)}')
    print()
    print(f'[SAMPLE-1] Message start at: {start_idx(SAMPLE_INPUT_1, 14)}')  # does not match example! 
    print(f'[SAMPLE-2] Message start at: {start_idx(SAMPLE_INPUT_2, 14)}')
    print(f'[SAMPLE-3] Message start at: {start_idx(SAMPLE_INPUT_3, 14)}')
    print(f'[SAMPLE-4] Message start at: {start_idx(SAMPLE_INPUT_4, 14)}')
    print(f'[REAL    ] Message start at: {start_idx(INPUT, 14)}')
