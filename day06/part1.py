from pathlib import Path
from collections import deque


if __name__ == "__main__":
    # Read text from input.txt
    text = Path("input.txt").read_text()

    # Record prev four characters
    prev = deque(maxlen=4)

    # Iterate over each character with index, adding to prev
    for i, c in enumerate(text):
        prev.append(c)

        # If we have four characters that are all different, break
        if len(set(prev)) == 4:
            break

    # Index +1 is answer
    print(i + 1)