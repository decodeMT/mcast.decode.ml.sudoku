"""
Sudoku solver algorithms

Author: Frankie Inguanez
Date: 15/01/2023

Implementation of naive brute force with backtracking sudoku solver algorithm.
"""
import sudokuUtils as spu

def findRandom(puzzle: list[list[int]]) -> tuple[int, int] | None:
    """
    Finds the next empty cell in a random fashion.
    """
    import random

    for row in random.sample(range(0,9),9):
        for col in random.sample(range(0,9),9):
            if puzzle[row][col] == 0:
                return (row, col)

    return None

def findByRow(puzzle: list[list[int]]) -> tuple[int, int] | None:
    """
    Finds the next empty cell in a raster fashion, row by row.
    Arguments:
        puzzle: a 9x9 sudoku puzzle
    """
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] == 0:
                return (row, col)
            
    return None

def findByCol(puzzle: list[list[int]]) -> tuple[int, int] | None:
    """
    Finds the next empty cell in a column order.
    Arguments:
        puzzle: a 9x9 sudoku puzzle
    """
    for col in range(0,9):
        for row in range(len(puzzle)):
            if puzzle[row][col]==0:
                return (row, col)
    
    return None

def findByBox(puzzle: list[list[int]], mode: int) -> tuple[int, int] | None:
    """
    Finds the next empty cell searching first by box then by row.
    Arguments:
        puzzle: a 9x9 sudoku puzzle
        mode:   4 searches for boxes sequentially, 
                5 searches for boxes in a zig-zag fashion, 
                6 searches for boxes in spiral fashion, 
                7 searches for boxes in a semi zig-zag fashion,
                8 searches for boxes randomly
    """
    import random

    if mode==4:
        boxes=range(0,9)
    elif mode==5:
        boxes=[0,1,2,5,4,3,6,7,8]
    elif mode==6:
        boxes=[0,1,2,5,8,7,6,3,4]
    elif mode==7:
        boxes=[0,1,4,3,6,7,8,5,2]
    elif mode==8:
        boxes=random.sample(range(0,9),9)
    elif mode==9:
        boxes=[0,4,8,1,2,3,5,6,7]
    else: return None

    for box in boxes:
        for row in range((box//3)*3,((box//3)*3)+3):
            for col in range((box%3)*3, ((box%3)*3)+3):
                if puzzle[row][col]==0:
                    return (row, col)

    return None

def findEmpty(puzzle: list[list[int]], search: int) -> tuple[int, int] | None:
    """
    Finds the next empty cell in a 9x9 sudoku puzzle.
    Arguments:
        puzzle: the 9x9 sudoku puzzle.
        search: defines how the puzzle is parsed: 
                    1 by row; 
                    2 by col; 
                    3 random;
                    4 by box sequentially; 
                    5 by box in a zig-zag; 
                    6 by box in a spiral; 
                    7 by box in a semi-zig-zag;
                    8 by box randomly;
                    9 by box diagonal;
    """
    if search==1:
        return findByRow(puzzle)
    elif search==2:
        return findByCol(puzzle)
    elif search==3:
        return findRandom(puzzle)
    elif search>=4 and search<=9:
        return findByBox(puzzle, search)
    
    return None

def getGuesses(validValues: list[int] | None, guess: int) -> list[int] | None:
    """
    Gets numbers to guess.
    Arguments:
        validValues: a dictionary of valid values.
        guess: the guessing mode. 1 for sequential, 2 for random.
    """
    if validValues is None:
        return None

    import random
    
    if guess==1:
        return validValues
    elif guess==2:
        return random.sample(validValues,len(validValues))

    return None

def solve(board: list[list[int]], validValues: dict[tuple[int, int], list[int]], history: list | None, stats: spu.SudokuStats | None, searchMode: int, guessMode: int):
    """
    Solves a 9x9 sudoku puzzle using backtracking algorithm.
    Arguments:
        board: the 9x9 puzzle to be solved.
        history: a list containing a history of solutions for tracking.
        stats: The statistics object to record algorithm.
        searchMode: the mode how the next empty cell is found.
        guessMode: the mode how the next number is guessed.
    """
    # Find the next empty cell
    find = findEmpty(board, searchMode)

    # If there is no empty cell than puzzle is complete
    if not find:
        return True
    else:
        row, col = find

    # Get numbers to guess and attempt
    if not validValues.__contains__((row,col)):
        return False

    vals = getGuesses(validValues.get((row, col)), guessMode)
    if vals is None:
        return False
        
    for guess in vals:
        if spu.isValid(board, guess, (row, col)):

            # Brute force guess
            if stats is not None:
                stats.incrementGuesses()

            board[row][col] = guess

            if history is not None:
                history.append(spu.toStr(board))

            # Attempt to solve rest of puzzle with current choice
            if solve(board, validValues, history, stats, searchMode, guessMode):
                return True

            # Invalid puzzle so backtrack
            if history is not None:
                history.remove(spu.toStr(board))

            if stats is not None:
                stats.incrementBacktracks()

            board[row][col] = 0

    return False