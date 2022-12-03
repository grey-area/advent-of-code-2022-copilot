from pathlib import Path


if __name__ == "__main__":
    # Read lines from input.txt
    lines = Path("input.txt").read_text().splitlines()

    # Loop over lines in groups of three, adding up score
    score = 0
    for i in range(0, len(lines), 3):
        group = lines[i:i+3]

        # Find the common letter in the group
        common = set(group[0]) & set(group[1]) & set(group[2])
        # Get the single letter
        letter = common.pop()

        # If it's lowercase, score is 1-26
        if letter.islower():
            score += ord(letter) - ord("a") + 1
        # If it's uppercase, score is 27-52
        else:
            score += ord(letter) - ord("A") + 27

    print(score)