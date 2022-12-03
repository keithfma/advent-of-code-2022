"""Reorganizing untidy rucksacks
"""

from pathlib import Path
from typing import Mapping


SAMPLE_INPUT = Path('sample-input.txt')
INPUT = Path('input.txt')


PRIORITIZED_ITEMS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
PRIORITY: Mapping = {x: idx for idx, x in enumerate(PRIORITIZED_ITEMS, start=1)}



def common_item(contents: str) -> str:
    """Return the single item that appear in both rucksack compartments
    """
    divider = len(contents) // 2
    left = set(contents[:divider])
    for item in contents[divider:]:
        if item in left:
            return item
    raise ValueError('No duplicate found!')



def total_common_item_priority(rucksack_path: Path) -> int:
    """Return the total priority of common items in all the elves' rucksacks
    """
    total_priority = 0
    with open(rucksack_path, 'r') as fp:
        for line in fp.readlines():
            item = common_item(line.strip())
            total_priority += PRIORITY[item]
    return total_priority


def badge(sacks: tuple[str, str, str]) -> str:
    """Find the single common item in the three input sacks
    """
    if len(sacks) != 3:
        raise ValueError('Expect 3 elves per group')
    intersection = set(sacks[0]) & set(sacks[1]) & set(sacks[2])
    if len(intersection) != 1:
        raise ValueError('Expect exactly one common item')
    return intersection.pop()


def total_badge_priority(rucksack_path: Path) -> int: 
    """Return the total priority of all 'badges' for the 3-elf groups
    """
    total_priority = 0
    with open(rucksack_path, 'r') as fp:
        while True:
            sacks = fp.readline().strip(), fp.readline().strip(), fp.readline().strip()
            if not sacks[0]:  # readline returns empty string at EOF
                break
            total_priority += PRIORITY[badge(sacks)]
    return total_priority
    

if __name__ == '__main__':

    print(f'[SAMPLE] Total priority of common items: {total_common_item_priority(SAMPLE_INPUT)}')
    print(f'[REAL  ] Total priority of common items: {total_common_item_priority(INPUT)}')
    print()
    print(f'[SAMPLE] Total priority of group badges: {total_badge_priority(SAMPLE_INPUT)}')
    print(f'[REAL  ] Total priority of group badges: {total_badge_priority(INPUT)}')
