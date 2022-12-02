"""Advent of Code 2022 - Day 1 - Calorie Counting
"""
from pathlib import Path


INPUT = Path('part-1-input.txt')


def max_calories_carried_by_one_elf(food_list_path):
    """Return the number of calories carried by the elf with the most calories
    """

    max_elf_calories = -1 
    elf_calories = 0

    with open(food_list_path, 'r') as fp:

        for line in fp.readlines():

            if line == '\n':
                # new elf!
                max_elf_calories = max(elf_calories, max_elf_calories)
                elf_calories = 0  

            else:
                elf_calories += int(line)

    return max_elf_calories


if __name__ == '__main__':

    print(f'Maximum calories carried by any elf: {max_calories_carried_by_one_elf(INPUT)}')
