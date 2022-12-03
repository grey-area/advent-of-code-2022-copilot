from pathlib import Path


if __name__ == "__main__":
    # Read lines from input.txt
    lines = Path("input.txt").read_text().splitlines()

    # Loop over lines, adding up score
    score = 0
    for line in lines:
        # Split line into first and second half by length
        first_half = line[:len(line) // 2]
        second_half = line[len(line) // 2:]

        # Find the element that appears in both halves (set ops)
        common = set(first_half) & set(second_half)

        # Get the single letter
        letter = common.pop()
        # If it's lowercase, score is 1-26
        if letter.islower():
            score += ord(letter) - ord("a") + 1
        # If it's uppercase, score is 27-52
        else:
            score += ord(letter) - ord("A") + 27

    print(score)