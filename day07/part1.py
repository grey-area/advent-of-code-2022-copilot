from pathlib import Path
from filesystem import FileSystem


if __name__ == "__main__":
    text = Path("input.txt").read_text()

    fs = FileSystem(text)

    # Find directories with size <= 100000
    # Print sum of sizes
    result = fs.find(lambda dir: dir.size <= 100000)
    print(sum(dir.size for dir in result))