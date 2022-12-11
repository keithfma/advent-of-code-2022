"""Advent of Code - Day ##
"""

from __future__ import annotations
from pathlib import Path
from attrs import frozen
from pprint import pprint
from collections import defaultdict


SAMPLE_INPUT = Path('sample-input.txt')
INPUT = Path('input.txt')


@frozen
class Tree:
    # note: including the (row, col) location so we don't have to 
    #   keep track of them when looking for visible trees, instead
    #   we can just store sets of Trees.
    height: int
    row: int
    col: int

    def __repr__(self) -> str:
        return f'Tree({self.height}, {self.row}, {self.col})'


def parse_trees(input_path: Path) -> list[list[Tree]]:
    """Read input file to a 2D array of Trees"""
    trees = []
    with open(input_path, 'r') as fp:
        for row, line in enumerate(fp.readlines()):
            trees.append(
                [
                    Tree(int(x), row, col) 
                    for col, x in enumerate(line.strip())
                ]
            )
    return trees
    


def _visible_from_left(trees: list[Tree]) -> set[Tree]:
    """Return the set of all trees that are visible from the 'left'
    (i.e., 0-index direction) side of the trees array
    """
    visible = {trees[0], trees[-1]}
    obstruction = 0
    for tree in trees:
        if tree.height > obstruction:
            visible.add(tree)
            obstruction = tree.height
    return visible


def _transpose(trees: list[list[Tree]]) -> list[list[Tree]]:
    """Return transpose of the input 2D array of trees"""
    columns = [[] for _ in range(len(trees))]
    for row in trees:
        for col, tree in enumerate(row):
            columns[col].append(tree)
    return columns


def count_visible_from_edges(trees: list[list[Tree]]) -> int:
    """Return the number of trees visible from the edges of the forest"""
    visible = set()

    for row in trees:
        visible.update(_visible_from_left(row))
        visible.update(_visible_from_left(row[::-1]))

    for col in _transpose(trees):
        visible.update(_visible_from_left(col))
        visible.update(_visible_from_left(col[::-1]))

    return len(visible)


def _score_to_right(trees: list[Tree]) -> dict[Tree, int]:
    """Return the 'scenic score' for all trees in the input array looking to the
    the right (i.e., max-index direction) of each
    """
    scores = {} 

    for idx, tree in enumerate(trees[:-1]):
        for distance, nbr_tree in enumerate(trees[idx+1:], 1):
            if nbr_tree.height >= tree.height:
                break
        scores[tree] = distance

    scores[trees[-1]] = 0  # edge always has 0 view

    return scores

def _merge_scores(total_scores: dict[Tree, int], direction_scores: dict[Tree, int]) -> None:
    """Merge score mapping from one direction into a total score mapping"""
    for tree, tree_score in direction_scores.items():
        if tree in total_scores: 
            total_scores[tree] *= tree_score
        else:
            total_scores[tree] = tree_score
    

def max_scenic_score(trees: list[list[Tree]]) -> int:
    """TODO"""
    total_scores = {}

    for row in trees:
        _merge_scores(total_scores, _score_to_right(row))
        _merge_scores(total_scores, _score_to_right(row[::-1]))

    for col in _transpose(trees):
        _merge_scores(total_scores, _score_to_right(col))
        _merge_scores(total_scores, _score_to_right(col[::-1]))

    return max(total_scores.values())



if __name__ == '__main__':

    sample = parse_trees(SAMPLE_INPUT)
    real = parse_trees(INPUT)

    print(f'[SAMPLE] Trees visible from edges: {count_visible_from_edges(sample)}')
    print(f'[REAL  ] Trees visible from edges: {count_visible_from_edges(real)}')
    print()
    print(f'[SAMPLE] Maximum scenic score: {max_scenic_score(sample)}')
    print(f'[REAL  ] Maximum scenic score: {max_scenic_score(real)}')
