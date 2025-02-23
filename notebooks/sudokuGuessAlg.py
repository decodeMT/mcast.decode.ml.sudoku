"""
Sudoku guess algorithms

Author: Frankie Inguanez
Date: 15/01/2023

A series of guess algorithms for sudoku puzzles.
"""

def getGuesses(puzzle, guessMode):
    """
    Gets numbers to guess.
    Arguments:
        puzzle: the 9x9 sudoku puzzle.
        guessMode: the guessing mode. 1 for sequential, 2 for random.
    """
    import random

    if guessMode==1:
        return range(1,10)
    elif guessMode==2:
        return random.sample(range(1,10),9)

    return None