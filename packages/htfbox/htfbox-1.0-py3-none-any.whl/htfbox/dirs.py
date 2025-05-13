from typing import Generator
import os

def walk_rel(path:str, include_dirs:bool=True, include_files:bool=True) -> Generator[str, None, None]:
    """I already know the root..."""

    for root, dirs, files in os.walk(path):

        if include_dirs:
            for d in dirs:
                full_path = os.path.join(root, d)
                rel_path = os.path.relpath(full_path, path)
                yield rel_path
        
        if include_files:
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, path)
                yield rel_path


def count_items(path:str, include_dirs:bool=True, include_files:bool=True) -> int:
    """How much folders and/or files are there?"""

    total = 0
    for _, dirs, files in os.walk(path):
        if include_dirs: total += len(dirs)
        if include_files: total += len(files)
    return total


def get_size(path:str) -> int:
    """How much space it takes?"""

    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            full_path = os.path.join(root, f)
            total += os.path.getsize(full_path)
    return total