"""Rock, paper, scissors tournament
"""

from types import MappingProxyType
from pathlib import Path
from typing import Mapping


# path to input file containing lines with [ABC] [XYZ] pairs representing a
#   rock-paper-scissors "strategy guide". It's meaning depends on the problem part
#   (i.e., 1 or 2)
INPUT = Path('input.txt')


# Scores according to part-1 interpretation of the strategy guide, i.e., 
#   that X is rock, Y is paper, and Z is scissors).
PART_1_SCORES = MappingProxyType(
    {
        ('A', 'X'): 1 + 3,  # rock     vs rock     + draw
        ('A', 'Y'): 2 + 6,  # rock     vs paper    + win
        ('A', 'Z'): 3 + 0,  # rock     vs scissors + lose 
        ('B', 'X'): 1 + 0,  # paper    vs rock     + lose 
        ('B', 'Y'): 2 + 3,  # paper    vs paper    + draw
        ('B', 'Z'): 3 + 6,  # paper    vs scissors + win
        ('C', 'X'): 1 + 6,  # scissors vs rock     + win
        ('C', 'Y'): 2 + 0,  # scissors vs paper    + lose
        ('C', 'Z'): 3 + 3,  # scissors vs scissors + draw
    }
)


# Scores according to part-2 interpretation of the strategy guide (i.e.,
#   X is lose, Y is draw, and Z is win). 
PART_2_SCORES = MappingProxyType(
    {
        ('A', 'X'): 0 + 3,  # opponent: rock     , outcome: lose, me: scissors  
        ('A', 'Y'): 3 + 1,  # opponent: rock     , outcome: draw, me: rock  
        ('A', 'Z'): 6 + 2,  # opponent: rock     , outcome: win , me: paper
        ('B', 'X'): 0 + 1,  # opponent: paper    , outcome: lose, me: rock 
        ('B', 'Y'): 3 + 2,  # opponent: paper    , outcome: draw, me: paper
        ('B', 'Z'): 6 + 3,  # opponent: paper    , outcome: win , me: scissors
        ('C', 'X'): 0 + 2,  # opponent: scissors , outcome: lose, me: paper
        ('C', 'Y'): 3 + 3,  # opponent: scissors , outcome: draw, me: scissors
        ('C', 'Z'): 6 + 1,  # opponent: scissors , outcome: win , me: rock
    }
)



def play(strategy_file: Path, scoring_table: Mapping) -> int:
    """Play rock-paper-scissors according the the "strategy guide" in stragegy_file, using
    scores from the lookup table in scoring_table. Return players total score.
    """
    my_score = 0
    with open(strategy_file, 'r') as fp:
        for line in fp.readlines():
            key = tuple(line.strip().split(' '))
            my_score += scoring_table[key]
    return my_score



if __name__ == '__main__':
    
    print(f'PART 1: My score is: {play(INPUT, PART_1_SCORES)}')
    print(f'PART 2: My score is: {play(INPUT, PART_2_SCORES)}')
