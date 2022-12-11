"""Advent of Code - Day 7
"""

from __future__ import annotations
from attrs import define
from pathlib import Path
from typing import Union, Optional


SAMPLE_INPUT = Path('sample-input.txt')
INPUT = Path('input.txt')


@define
class Folder:

    name: str
    parent: Optional[Folder]
    children: list[Union[Folder, File]]
    _size: Optional[int] = None

    @property
    def size(self) -> None:
        if self._size is None:
            self._size = sum(x.size for x in self.children)   
        return self._size

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.name}, {self.size}")'


@define
class File:

    name: str
    parent: Folder
    size: int

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.name}, {self.size}")'


def inspect_disk(terminal_output_path: Path) -> Folder:
    """Parse text of terminal commands and thier output to discover the file tree
    Return the root folder of this file tree.
    """

    root = Folder('/', None, [], None)
    pwd = root

    with open(terminal_output_path, 'r') as fp:

        while line := fp.readline().strip():

            if line.startswith('$ cd'):
                _, __, name = line.split()

                if name == '..':
                    pwd = pwd.parent

                else:

                    for child in pwd.children:
                        if child.name == name:
                            pwd = child
                    if pwd.name != name:
                        raise ValueError(f'Command failed: {line}')
                

            elif line.startswith('$ ls'):
                pass
            
            elif line.startswith('dir'):
                # define new folder
                _, name = line.split(' ')
                pwd.children.append(Folder(name, pwd, [], None))

            else:
                # define new file
                size_txt, name =  line.split(' ')
                pwd.children.append(File(name, pwd, int(size_txt)))

    return root


def display_disk(f: Union[Folder, File], indent: int = 0) -> None:
    """Pretty-print file tree starting from location 'f' at indent 'indent'
    """
    print('  '*indent + f'- {f}')
    if isinstance(f, Folder):
        for child in f.children:
            display_disk(child, indent + 1)


def sum_below_threshold(f: Folder, threshold: int) -> int:
    """Return sum of sizes of all folders below a threshold size
    """
    total = 0
    if f.size < threshold:
        total += f.size
    for child in f.children:
        if isinstance(child, Folder):
            total += sum_below_threshold(child, threshold)
    return total


def all_folders(f: Folder) -> list[Folder]:
    """Return all subfolders of the 'f', recursively descending into children
    """
    folders = [f]
    for child in f.children:
        if isinstance(child, Folder):
            folders.extend(all_folders(child))
    return folders


def smallest_sufficient_folder(root: Union[File, Folder]) -> Folder:
    """Return the smallest folder under 'root' that we can delete to free the minimum disk space
    """
    disk_size = 70_000_000
    min_empty_space = 30_000_000
    space_to_free = min_empty_space - (disk_size - root.size)

    candidates = [x for x in all_folders(root) if x.size >= space_to_free]
    return sorted(candidates, key=lambda x: x.size)[0]


if __name__ == '__main__':

    sample_root = inspect_disk(SAMPLE_INPUT)
    root = inspect_disk(INPUT)
    
    print(f'[SAMPLE] Total size of folders below threshold size: {sum_below_threshold(sample_root, 100_000)}')
    print(f'[REAL  ] Total size of folders below threshold size: {sum_below_threshold(root, 100_000)}')
    print()
    print(f'[SAMPLE] Size of the smallest folder we can delete: {smallest_sufficient_folder(sample_root)}')
    print(f'[REAL  ] Size of the smallest folder we can delete: {smallest_sufficient_folder(root)}')


    all_folders(sample_root)

