from pathlib import Path
import re
from dataclasses import dataclass


# Input text is like
"""    [D]
[N] [C]
[Z] [M] [P]
 1   2   3 """
# Meaning stack 1 has N,Z, stack 2 has C,M,D stack 3 has P
def parse_stacks(stacks_text):
    # regex to find [A] [B] [C] etc
    pattern = re.compile(r'\[([A-Z])\]')

    # Split text into lines
    lines = stacks_text.split('\n')

    # Number of ints on last line tells us how many stacks there are
    num_stacks = len(lines[-1].split())

    # Loop over other lines, build stacks
    stacks = [[] for _ in range(num_stacks)]
    for line in lines[:-1]:
        # Find all matches including their positions in the string
        # (to get actual position divide by 4)
        matches = pattern.finditer(line)
        for match in matches:
            letter = match.group(1)
            position = match.start() // 4
            # Add to stacks dict
            stacks[position].append(letter)

    # Reverse stacks
    stacks = [stack[::-1] for stack in stacks]
    return stacks


# Dataclass for moving number of blocks from src to dst
@dataclass
class Move:
    num: int
    src: int
    dst: int


# Input text is like
def parse_moves(moves_text):
    # Regex to find pattern like "move 1 from 2 to 1"
    pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')
    moves = [Move(*map(int, match.groups())) for match in pattern.finditer(moves_text)]
    return moves


def parse_text(text):
    # Split on double new line to get stacks text and moves text
    stacks_text, moves_text = text.split('\n\n')
    stacks = parse_stacks(stacks_text)
    moves = parse_moves(moves_text)
    return stacks, moves


# Function to process single move (note, because multiple blocks can be moved
# at the same time, there's no need to reverse order of moved blocks)
def process_move(stacks, move):
    # Get src and dst stacks
    src_stack = stacks[move.src - 1]
    dst_stack = stacks[move.dst - 1]

    # Get blocks to move
    blocks = src_stack[-move.num:]

    # Remove blocks from src stack
    src_stack[-move.num:] = []

    # Add blocks to dst stack
    dst_stack.extend(blocks)


if __name__ == "__main__":
    # Parse input.txt to get stacks and moves
    stacks, moves = parse_text(Path("input.txt").read_text())

    # Process moves
    for move in moves:
        process_move(stacks, move)

    # Get the top of each stack, concatenate to get final string
    final_string = ''.join([stack[-1] for stack in stacks])
    print(final_string)