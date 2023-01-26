"""
Data cleaning and Util functions

Author: Frankie Inguanez
Date: 13/01/2023

A series of utility functions to clean and check a sudoku puzzle.
"""
class SudokuStats:
    def __init__(self):
        self.guesses = 0
        self.backtracks = 0
        self.executionTime = None
        self.unknowns = 0

    def incrementGuesses(self):
        self.guesses += 1

    def incrementBacktracks(self):
        self.backtracks += 1

    def registerExecutionTime(self, executionTime):
        self.executionTime=executionTime

    def setUnknowns(self, zeros:int):
        self.unknowns=zeros

def getFileLineCount(fileName: str):
    """
    Get number of lines in a file.
    Arguments:
        fileName: the name of the file to process.
    """
    import mmap

    lines = 0
    with open(fileName, "r+", encoding="utf-8") as f:
        bf = mmap.mmap(f.fileno(), 0)

        while bf.readline():
            lines += 1

    return lines
    
def saveError(error, errorsFileName: str):
    """
    Saves an error/exception that is raised.
    Arguments:
        error: the Exception that is raised.
        errorsFileName: the file name where the error will be saved.
    """
    try:
        with open(errorsFileName, "a", encoding="utf-8") as ef:
            ef.write("Encountered error:\n{}\n{}\n{}\n\n".format(type(error), error.args, error))
    except Exception as e:
        # Failed to save error to file
        print("Failed to save original error to file due to:\n{}\n{}\n{}\n\n".format(type(e), e.args, e))
        print("Original error:\n{}\n{}\n{}\n\n".format(type(error), error.args, error))
        
def to2DArray(n: str):
    """
    Convert a string to a 2D 9x9 array.
    Arguments:
        n: an 81 digits in string format.
    """
    return [list(map(int, n[i:i+9])) for i in range(0, 81, 9)]

def toStr(puzzle):
    """
    Converts a puzzle to a string.
    Arguments:
        puzzle: a 2 dimensional array representing the 9x9 puzzle. 
    """
    r = str()

    for row in puzzle:
        r += "".join(map(str, row))

    return r

def getColValues(puzzle, col: int):
    """
    Get column values.
    Arguments:
        puzzle: a 2 dimensional array representing the 9x9 puzzle. 
        col: the column number.
    """
    lst = list()
    for row in puzzle:
        lst.append(row[col])

    return lst

def getBox(row:int, col:int):
    """
    Returns the box identification number based on row and col number.
    Arguments:
        row: the row number.
        col: the column number.
    """
    return (row//3)*3+ col//3

def getBoxValues(puzzle, box: int):
    """
    Get box values. Boxes are 3x3 sub-grids enumerates from top left in a raster fashion
    0, 1, 2
    3, 4, 5
    6, 7, 8
    Arguments:
        puzzle: a 2 dimensional array representing the 9x9 puzzle.
        box: the box identification number.
    """
    return [puzzle[x][y] for x in range((box//3)*3,((box//3)*3)+3) for y in range((box%3)*3, ((box%3)*3)+3)]

def checkList(lst: list):
    """
    Checks if a list contains all numbers from 1 to 9.
    Arguments:
        lst: the list of numbers.
    """
    return set(lst) == set(range(1,10))

def isSolved(puzzle):
    """
    Check if a puzzle has been solved.
    Arguments:
        puzzle: a 2 dimensional array representing the 9x9 puzzle.
    """
    # Check rows
    for row in puzzle:
        if not checkList(row):
            return False

    # Check columns
    for i in range(0,9):
        if not checkList(getColValues(puzzle, i)):
            return False;

    # Check box
    for i in range(0,9):
        if not checkList(getBoxValues(puzzle, i)):
            return False;

    return True

def isValid(puzzle, num: int, pos):
    """
    Checks if a number can be added to a specific position
    Arguments:
        puzzle: a 2 dimensional array representing the 9x9 puzzle.
        num: the number to insert.
        pos: the row and column position to place the digit.
    """ 
    # Check the row
    for i in range(len(puzzle[0])):
        if puzzle[pos[0]][i]==num and pos[1] != i:
            return False

    # Check the column
    for i in range(len(puzzle[1])):
        if puzzle[i][pos[1]]==num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if puzzle[i][j] == num and (i,j) != pos:
                return False

    return True

def allowedValues(board,row,col):
    """
    Gets all allowed values for a given position in a board.
    Arguments:
        board: a 2 dimensional 9x9 sudoku puzzle.
        row: the row number.
        col: the column number.
    """
    result = list()

    for number in range(1,10):
        nums = board[row]
        if number in nums:
            continue

        nums = getColValues(board, col)
        if number in nums:
            continue
        
        nums = getBoxValues(board, getBox(row,col))
        if number in nums:
            continue

        result.append(number)

    return result

def cacheValidValues(board):
    """
    Creates a cache of possible values for each cell in a board.
    Arguments:
        board: a 2 dimensional array of a 9x9 sudoku board.
    """
    cache = dict()
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                cache[(i,j)] = allowedValues(board,i,j)
    return cache