from pathlib import Path
from filesystem import FileSystem


if __name__ == "__main__":
    terminal_text = Path("input.txt").read_text()

    fs = FileSystem(terminal_text)

    free_space_required = 30000000
    space_to_free = free_space_required - fs.free_space

    # Find candidate directories to delete
    deletion_candidates = fs.find(lambda dir: dir.size >= space_to_free)
    # Get the size of the smallest of these
    smallest_size = min(dir.size for dir in deletion_candidates)
    print(smallest_size)