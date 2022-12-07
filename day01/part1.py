from pathlib import Path


if __name__ == "__main__":
    # Read the text
    text = Path("input.txt").read_text()

    # Split by blank lines
    groups = text.split("\n\n")

    # Parse each line in each group as an int, and compute sum for each group
    sums = [sum(map(int, group.split())) for group in groups]

    # Print the max
    print(max(sums))