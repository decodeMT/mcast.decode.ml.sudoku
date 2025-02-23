"""
Sudoku solver algorithms

Author: Frankie Inguanez
Date: 15/01/2023

A series of solution algorithms for sudoku puzzles.
"""

import sudokuSearchAlg as ssa
import sudokuGuessAlg as sga
import sudokuPuzzleUtils as spu

def backtracking(board: list, history: list, stats: spu.SudokuStats, config: spu.SudokuConfig):
    """
    Solves a 9x9 sudoku puzzle using backtracking algorithm.
    Arguments:
        board: the 9x9 puzzle to be solved.
        stats: The statistics object to record algorithm.
        searchMode: defines how the puzzle is parsed: 1 by row; 2 by col; 3 by box sequentially; 4 by box in a zig-zag; 5 by box in a spiral; 6 by box in a semi-zig-zag
        guessMode: defines how numbers are guessed: 1 sequentially; 2 randomly
    """
    # Find the next empty cell
    find = ssa.findEmpty(board, config.searchMode)

    # If there is no empty cell than puzzle is complete
    if not find:
        return True
    else:
        row, col = find

    # Get numbers to guess and attempt
    for guess in sga.getGuesses(board, config.guessMode):
        if spu.isValid(board, guess, (row, col)):

            # Brute force guess
            stats.incrementGuesses()
            board[row][col] = guess

            if config.tracking:
                history.append(spu.toStr(board))

            # Attempt to solve rest of puzzle with current choice
            if backtracking(board, history, stats, config):
                return True

            # Invalid puzzle so backtrack
            if config.tracking:
                history.remove(spu.toStr(board))
            stats.incrementBacktracks()
            board[row][col] = 0

    return False
