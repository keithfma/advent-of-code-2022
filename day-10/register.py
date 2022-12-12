"""Advent of Code - Day 10
"""

from __future__ import annotations
from pathlib import Path
from attrs import define, evolve


SAMPLE_INPUT_1 = Path('sample-input-1.txt')
SAMPLE_INPUT_2 = Path('sample-input-2.txt')
INPUT = Path('input.txt')


@define
class State:
    """The state of the register **during** the specified cycle
    """
    register: int
    cycle: int


@define
class Instruction:
    """An instruction taking 'num_cycles' and then incrementing the register by 'increment'
    """
    num_cycles: int
    increment: int



def parse_ops(input_file: Path) -> Generator[Instruction, None, None]:
    """Generator returning a sequence of operations from the input file
    """
    with open(input_file, 'r') as fp:
        for line in fp.readlines():
            if line.startswith('noop'):
                yield Instruction(num_cycles=1, increment=0)
            elif line.startswith('addx'):
                yield Instruction(num_cycles=2, increment=int(line.strip().split(' ')[1]))


def execute_ops(input_file: Path) -> Generator[State, None, None]:
    """Generator returning a sequence of states reached by applying operations from the input file
    """
    # initial state during cycle 0
    state = State(register=1, cycle=0)
    yield state

    for op in parse_ops(input_file):
        for _ in range(op.num_cycles):
            # during cycle, update cycle number but not the register
            state = evolve(state, cycle=state.cycle + 1)
            yield state
        # end of cycle, update the register   
        state = evolve(state, register=state.register + op.increment)

    # final state during the cycle after the completion of the last instruction
    state = evolve(state, cycle=state.cycle + 1)
    yield state


def sum_of_strengths(input_file: Path) -> int:
    """Return the total 'strength' at key cycles"""
    total_strength = 0
    key_cycles = {20, 60, 100, 140, 180, 220}
    for state in execute_ops(input_file):
        if state.cycle in key_cycles:
            total_strength += state.register * state.cycle
    return total_strength


def render_screen(input_file: Path) -> None:
    """Display the ascii-art image represented by the operations in the input file
    """
    crt_line_length = 40

    for state in execute_ops(input_file):

        crt_position = (state.cycle - 1) % crt_line_length
        
        if crt_position == 0:
            # start new line
            print('\n', end='')

        if abs(crt_position - state.register) <= 1:
            # pixel is lit
            print('#', end='')
        else:
            # pixel is dark 
            print('-', end='')



if __name__ == '__main__':

    print(f'[SAMPLE-2] Total signal strength: {sum_of_strengths(SAMPLE_INPUT_2)}')
    print(f'[REAL    ] Total signal strength: {sum_of_strengths(INPUT)}')

    print()
    print(f'[SAMPLE-2]')
    render_screen(SAMPLE_INPUT_2)

    print()
    print(f'[REAL]')
    render_screen(INPUT)
