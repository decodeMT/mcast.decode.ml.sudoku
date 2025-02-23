"""
Sudoku Puzzle generator

Author: Frankie Inguanez
Date: 16/01/2023

A sudoku puzzle generator.
"""
import random
import sudokuPuzzleUtils as spu
import sudokuSolvers as solver

def generatePuzzle(count: int, zeros: int):
    """
    Generates a number of 9x9 sudoku puzzle grid with a pre-defined number of zeros (unknowns).
    Arguments:
        count: the number of puzzles to generate.
        zeros: the number of zeros desired in each puzzle.
    """
    puzzles = []
    for i in range(count):
        puzzle = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'

        board = spu.to2DArray(puzzle)
        stats = spu.SudokuStats()
        stats.setUnknowns(puzzle.count('0'))
        config = spu. SudokuConfig(searchMode=9, guessMode=2, tracking=False)
        solver.backtracking(board, None, stats, config)

        # Remove digits
        changed = 0
        while changed < zeros:
            row = random.sample(range(0,9),1)[0]
            col = random.sample(range(0,9),1)[0]
            
            if board[row][col]==0:
                continue

            board[row][col]=0
            changed+=1
            
        puzzles.append(spu.toStr(board))

    return puzzles