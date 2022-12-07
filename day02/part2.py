from pathlib import Path


if __name__ == "__main__":
    # Read lines from the input file
    lines = Path("input.txt").read_text().splitlines()

    # Lines are like A X
    # Left hand side is opponents play A=rock, B=paper, C=scissors
    # Setup opponent play dict
    opponent_play_dict = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}

    # Right hand side is whether I win, lose, or draw
    # X = lose, Y = draw, Z = win
    # 6 points for a win, 3 for a draw, 0 for a loss
    # Setup score dict
    score_dict = {'X': 0, 'Y': 3, 'Z': 6}

    # Indices for rock, paper, scissors
    rock_paper_scissors_indices = {'rock': 0, 'paper': 1, 'scissors': 2}

    # This next dict gives the offset from the opponents index given the result
    offset_dict = {'X': -1, 'Y': 0, 'Z': 1}

    # Loop over lines and play the game
    score = 0
    for line in lines:
        opponent, result = line.split()
        opponent_play = opponent_play_dict[opponent]

        # win=6, draw=3, lose=0
        score += score_dict[result]

        # compute the index of my play given the index of the opponent's play
        # and the offset
        my_play_index = (rock_paper_scissors_indices[opponent_play] + offset_dict[result]) % 3

        # 1 point for playing rock, 2 for paper, 3 for scissors
        score += my_play_index + 1

    print(score)