"""
Sudoku search algorithms

Author: Frankie Inguanez
Date: 15/01/2023

A series of search algorithms for sudoku puzzles.
"""

def findRandom(puzzle):
    """
    Finds the next empty cell in a random fashion.
    """
    import random

    for row in random.sample(range(0,9),9):
        for col in random.sample(range(0,9),9):
            if puzzle[row][col] == 0:
                return (row, col)

    return None

def findByRow(puzzle):
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

def findByCol(puzzle):
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

def findByBox(puzzle, mode):
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

    for box in boxes:
        for row in range((box//3)*3,((box//3)*3)+3):
            for col in range((box%3)*3, ((box%3)*3)+3):
                if puzzle[row][col]==0:
                    return (row, col)

    return None

def findEmpty(puzzle, searchMode):
    """
    Finds the next empty cell in a 9x9 sudoku puzzle.
    Arguments:
        puzzle: the 9x9 sudoku puzzle.
        searchMode: defines how the puzzle is parsed: 
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
    if searchMode==1:
        return findByRow(puzzle)
    elif searchMode==2:
        return findByCol(puzzle)
    elif searchMode==3:
        return findRandom(puzzle)
    elif searchMode>=4 and searchMode<=9:
        return findByBox(puzzle, searchMode)
    
    return None