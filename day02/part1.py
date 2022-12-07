from pathlib import Path


if __name__ == "__main__":
    # Read lines from the input file
    lines = Path("input.txt").read_text().splitlines()

    # Lines are like A X
    # Left hand side is opponents play A=rock, B=paper, C=scissors
    # Right hand side is my play X=rock, Y=paper, Z=scissors

    # Set up the play dictionaries
    opponent_play_dict = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}
    my_play_dict = {'X': 'rock', 'Y': 'paper', 'Z': 'scissors'}

    # Indices for rock, paper, scissors
    rock_paper_scissors_indices = {'rock': 0, 'paper': 1, 'scissors': 2}

    # Loop over lines and play the game
    score = 0
    for line in lines:
        opponent, me = line.split()
        opponent_play = opponent_play_dict[opponent]
        my_play = my_play_dict[me]

        # win=6, draw=3, lose=0
        # without if statements
        score += 3 * ((rock_paper_scissors_indices[my_play] - rock_paper_scissors_indices[opponent_play] + 1) % 3)

        # 1 point for playing rock, 2 for paper, 3 for scissors
        score += rock_paper_scissors_indices[my_play] + 1

    print(score)