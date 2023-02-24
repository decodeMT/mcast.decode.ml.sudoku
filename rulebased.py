"""
Sudoku solver algorithm

Author: Frankie Inguanez
Date: 15/01/2023

Implementation of rule-based with backtracking sudoku solver algorithm.
"""
import sudokuPuzzleUtils as spu

def removeValueInRow(validValues: dict[tuple[int, int], list[int]], row: int, val: int):
    """
    Removes a value from the valid values dictionary for an entire row.
    Arguments:
        validValues: the current cache of valid values.
        row: the row identification number.
        val: the value to remove.
    """
    for pos in validValues:
        if pos[0]!=row:
            continue

        vals = validValues.get(pos)
        if vals is None:
            continue

        if vals.__contains__(val):
            vals.remove(val)
            validValues[pos]= vals

def removeValueInCol(validValues: dict[tuple[int, int], list[int]], col: int, val: int):
    """
    Removes a value from the valid values dictionary for an entire column.
    Arguments:
        validValues: the current cache of valid values.
        col: the column identification number.
        val: the value to remove.
    """
    for pos in validValues:
        if pos[1]!=col:
            continue

        vals = validValues.get(pos)
        if vals is None:
            continue

        if vals.__contains__(val):
            vals.remove(val)
            validValues[pos]= vals

def removeValueInBox(validValues: dict[tuple[int, int], list[int]], pos: tuple[int,int], val: int):
    """
    Removes a value from the valid values dictionary for an entire column.
    Arguments:
        validValues: the current cache of valid values.
        pos: the position being investigated.
        val: the value to remove.
    """
    positions = spu.getBoxPositionsByPos(pos)
    for position in positions:
        vals = validValues.get(position)
        if vals is None:
            continue
        
        if vals.__contains__(val):
            vals.remove(val)
            validValues[position] = vals

def updateBoard(board: list[list[int]], validValues: dict[tuple[int, int], list[int]], history: list[str] | None, pos: tuple[int,int], val: int):
    """
    Updates the board and valid values.
    Arguments:
        board: the 9x9 sudoku board.
        validValues: a dictionary with valid values for unfilled positions in the board.
        history: a history of solutions.
        pos: the row and column position to be filled in.
        val: the value to be inserted.
    """
    board[pos[0]][pos[1]]=val

    if history is not None:
        history.append(spu.toStr(board))

    removeValueInRow(validValues, pos[0], val)
    removeValueInCol(validValues, pos[1], val)
    removeValueInBox(validValues, pos, val)

def solveNakedSingle(board: list[list[int]], validValues: dict[tuple[int, int], list[int]], history: list[str] | None) -> bool:
    """
    Identifies if a single valid value is possible in a cell and applies it.
    Arguments:
        board: the sudoku puzzle to process.
        validValues: a dictionary with valid values for various positions.
        history: a log of solutions.
    """
    posToDel = list[tuple[int,int]]()
    for pos in validValues:
        vals = validValues.get(pos)
        if vals is None:
            continue
        
        if vals.__len__()== 1:
            updateBoard(board, validValues, history, pos, vals[0])
            posToDel.append(pos)

    # Remove all positions from the dictionary now and not before so not to change the structure during the loop
    for pos in posToDel:
        del validValues[pos]

    # Return if a change took place
    return posToDel.__len__()>0

def findLoneRanger(vals: list[int], positions: dict[int, list[tuple[int,int]]], pos: tuple[int, int]):
    """
    Finds the position of a cells that have lone rangers.
    Arguments:
        vals: the valid values.
        positions: a dictionary containing the positions where values are possible.
        pos: the position being considered
    """
    for val in vals:
        # Get the current valid positions for the current value
        cells = list[tuple[int, int]]()
        current = positions.get(val)
        if current is not None:
            cells.extend(current)

        # Add the current cell and update
        cells.append(pos)
        positions[val]=cells

def applyLoneRanger(board: list[list[int]], validValues: dict[tuple[int, int], list[int]], history: list[str] | None, positions: dict[int, list[tuple[int,int]]], posToDel: list[tuple[int,int]]):
    """
    Applies the lone ranger logic, thus solving a cell and updating the valid values.
    Arguments:
        board: the 9x9 sudoku board.
        validValues: the valid values on the board for unsolved cells.
        history: the history of solutions.
        positions: the positions where values are possible in a specific axis (row, column or box).
        posToDel: the list of position to remove.
    """
    for val in positions:
        cells = positions.get(val)
        if cells is None:
            continue

        if cells.__len__() != 1:
            continue

        updateBoard(board, validValues, history, cells[0], val)
        posToDel.append(cells[0])

def solveLoneRanger(board: list[list[int]], validValues: dict[tuple[int, int], list[int]], history: list[str] | None) -> bool:
    """
    Identifies if a value is possible in only one cell.
    Arguments:
        board: the sudoku puzzle to process.
        validValues: a dictionary with valid values for various positions.
        history: a log of solutions.
    """
    posToDel = list[tuple[int,int]]()

    # Search by row and register the positions for each valid value in each column
    for row in range(0,9):
        positions = dict[int, list[tuple[int,int]]]()
        for col in range(0, 9):
            # Get the valid values for the current cell
            vals = validValues.get((row, col))
            if vals is None:
                continue

            findLoneRanger(vals, positions, (row, col))

        applyLoneRanger(board, validValues, history, positions, posToDel)

    # Search by col
    for col in range(0, 9):
        positions = dict[int, list[tuple[int,int]]]()
        for row in range(0, 9):
            # Get the valid values for the current cell
            vals = validValues.get((row, col))
            if vals is None:
                continue

            findLoneRanger(vals, positions, (row, col))

        applyLoneRanger(board, validValues, history, positions, posToDel)

    # Search by box
    for box in range(0,9): 
        positions = dict[int, list[tuple[int,int]]]()
        for pos in spu.getBoxPositions(box):
            # Get the valid values for the current cell
            vals = validValues.get(pos)
            if vals is None:
                continue

            findLoneRanger(vals, positions, pos)

        applyLoneRanger(board, validValues, history, positions, posToDel)

    # Remove all positions from the dictionary now and not before so not to change the structure during the loop
    for pos in posToDel:
        del validValues[pos]

    # Return if a change took place
    return posToDel.__len__()>0

def solve(board: list[list[int]], validValues: dict[tuple[int,int], list[int]], history: list[str], stats: spu.SudokuStats | None, searchMode: int, guessMode: int) -> bool:
    """
    Solves a sudoku puzzle by using some rules, then backtracking when guesses are needed.
    Arguments:
        board: the 9x9 puzzle to be solved.
        validValues: the possible values for each unsolved cell.
        history: a list containing a history of solutions for tracking.
        stats: The statistics object to record algorithm.
        searchMode: the mode how the next empty cell is found.
        guessMode: the mode how the next number is guessed.
    """
    while True:
        # Check for naked single
        if solveNakedSingle(board, validValues, history):
            continue

        # Check for lone ranger
        if solveLoneRanger(board, validValues, history):
            continue

        # TODO: implement more rules

        # No cell was solved so only guesses left or puzzle is solved
        break

    # Check if puzzle is solved
    if spu.isSolved(board):
        return True

    # Only guesses are left so solve using backtracking
    import backtracking as bk
    return bk.solve(board, validValues, history, stats=stats, searchMode=searchMode, guessMode=guessMode)  