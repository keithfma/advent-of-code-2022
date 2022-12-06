"""Advent of Code - Day ##
"""
from attrs import frozen, field
from pathlib import Path
import re
from pprint import pprint


SAMPLE_INPUT = Path('sample-input.txt')
INPUT = Path('input.txt')


@frozen
class Instruction:
    count: int = field(converter=int)
    from_stack: int = field(converter=int)
    to_stack: int = field(converter=int)


def parse_input(input_path: Path): 
    """Parse input file and return:
    * dictionary mapping stack label to a list of the crates in the stack
    * list of instructions for moving crates bewteen stacks
    """
    with open(input_path, 'r') as fp:
        
        # read lines until stack labels are reached
        lines = []
        while not re.match(r'^.*\d', line := fp.readline()):
            lines.append(line)

        # allocate lookups for stack indices and stack contents
        num_stacks = int(line.strip()[-1])
        stacks = {x: [] for x in range(1, num_stacks+1)}
        stacks_idx = {x: 1 + 4*(x-1) for x in range(1, num_stacks+1)}

        # populate stacks, bottom elements are first in the stack list
        for line in reversed(lines):
            for x in stacks:
                crate = line[stacks_idx[x]].strip()
                if crate:
                    stacks[x].append(crate)

        # continue on to read instructions
        instructions = []
        fp.readline()  # skip one
        for line in fp.readlines():
            instructions.append(
                Instruction(
                    *re.match(r'move (\d+) from (\d+) to (\d+)', line).groups()
                )
            )

        return stacks, instructions


def crate_mover_9000(stacks, instructions):
    """Apply instructions to the input stacks (mutating the stacks in the process)
    Return the top crate from each stack (in order)
    """
    for i in instructions:
        for _ in range(i.count):
            stacks[i.to_stack].append(stacks[i.from_stack].pop())
    
    crates = []
    for k in sorted(stacks.keys()):
        crates.append(stacks[k][-1])

    return ''.join(crates)

        
def crate_mover_9001(stacks, instructions):
    """Apply instructions to the input stacks (mutating the stacks in the process)
    Return the top crate from each stack (in order)
    """
    for i in instructions:
        in_transit = stacks[i.from_stack][-i.count:]
        stacks[i.from_stack] = stacks[i.from_stack][:-i.count]
        stacks[i.to_stack].extend(in_transit)
    
    crates = []
    for k in sorted(stacks.keys()):
        crates.append(stacks[k][-1])

    return ''.join(crates)


if __name__ == '__main__':

    print(f'[SAMPLE]: top crates are: {crate_mover_9000(*parse_input(SAMPLE_INPUT))}')
    print(f'[REAL  ]: top crates are: {crate_mover_9000(*parse_input(INPUT))}')

    print(f'[SAMPLE]: top crates are: {crate_mover_9001(*parse_input(SAMPLE_INPUT))}')
    print(f'[REAL  ]: top crates are: {crate_mover_9001(*parse_input(INPUT))}')
        
    


                 

    
