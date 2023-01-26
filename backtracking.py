"""
Sudoku solver algorithms

Author: Frankie Inguanez
Date: 15/01/2023

Implementation of naive brute force with backtracking sudoku solver algorithm.
"""
import sudokuPuzzleUtils as spu

def getSearchAlg(searchMode: int):
    """
    Translates a numeric search mode to text.
    Arguments:
        searchMode: the numeric identifier for the search mode.
    """
    if (searchMode==1):
        return "By Row"
    elif (searchMode==2):
        return "By Column"
    elif (searchMode==3):
        return "Random"
    elif (searchMode==4):
        return "By mini-grid sequential"
    elif (searchMode==5):
        return "By mini-grid zig-zag"
    elif (searchMode==6):
        return "By mini-grid sprial"
    elif (searchMode==7):
        return "By mini-grid semi zig-zag"
    elif (searchMode==8):
        return "By mini-grid randomly"
    elif (searchMode==9):
        return "By box diagonal"
    else: return "Unknown" 

def getGuessAlg(guessMode: int):
    """
    Translates a numeric guess mode to text.
    Arguments:
        guessMode: the numeric identifier for the guess mode.
    """
    if (guessMode==1):
        return "Sequential"
    elif (guessMode==2):
        return "Random"
    else: "Unknown"

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

def findEmpty(puzzle, search):
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

def getGuesses(validValues: list, guess: int):
    """
    Gets numbers to guess.
    Arguments:
        validValues: a dictionary of valid values.
        guess: the guessing mode. 1 for sequential, 2 for random.
    """
    import random

    if guess==1:
        return validValues
    elif guess==2:
        return random.sample(validValues,len(validValues))

    return None

def backtracking(board: list, validValues: dict, history: list, stats: spu.SudokuStats, searchMode: int, guessMode: int):
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
    for guess in getGuesses(validValues.get((row, col)), guessMode):
        if spu.isValid(board, guess, (row, col)):

            # Brute force guess
            if stats is not None:
                stats.incrementGuesses()

            board[row][col] = guess

            if history is not None:
                history.append(spu.toStr(board))

            # Attempt to solve rest of puzzle with current choice
            if backtracking(board, validValues, history, stats, searchMode, guessMode):
                return True

            # Invalid puzzle so backtrack
            if history is not None:
                history.remove(spu.toStr(board))

            if stats is not None:
                stats.incrementBacktracks()

            board[row][col] = 0

    return False

def solve(  puzzlesFileName: str, solutionsFileName: str, statsFileName: str, trackingFileName: str, errorsFileName: str, \
            offset: int, limit: int, search: int, guess: int):
    """
    Solves puzzles found in a file using backtracking algorithm.
    Arguments:
        puzzlesFileName: the file name containing puzzles
        solutionsFileName: the file name where to store the solutions.
        statsFileName: the file name where to store the statistics.
        trackingFileName: the file name where tracking is saved.
        errorsFileName: the file name where errors shall be saved.
        offset: the number of puzzles to offset.
        limit: the limit number of puzzles to solve.
        search: defines how missing values are searched.
        guess: defines how guesses are made.
    """
    import tqdm
    import timeit

    if not limit:
        limit = spu.getFileLineCount(puzzlesFileName)
    else: limit = limit

    i = 1
    hasError = False
    try:
        # Open statistics file and Write header row
        if statsFileName is not None:
            with open(statsFileName, "w", encoding="utf-8") as sf:
                sf.write("Puzzle,Solution,Execution Time,Zeros,Guesses,Backtracks\n")

        # Open puzzles and read till limit is reached.
        with open(puzzlesFileName, "r", encoding="utf-8") as pf:
            for line in tqdm.tqdm(pf, total=limit):
                # Stop at limit
                if (i>limit):
                    break

                # Create board and statistics
                puzzle=line.strip()
                board = spu.to2DArray(puzzle)
                
                history = list()
                stats = spu.SudokuStats();
                stats.setUnknowns(puzzle.count('0'))
                validValues = spu.cacheValidValues(board)
                stats.registerExecutionTime(timeit.timeit(lambda: backtracking(board, validValues, history, stats, search, guess), number=1000))                   
                
                # Write solution
                if solutionsFileName is not None:
                    with open(solutionsFileName, "a", encoding="utf-8") as af:
                        af.write("{}\n".format(spu.toStr(board)))

                # Write history
                if trackingFileName is not None:
                    with open(trackingFileName, "a", encoding="utf-8") as tf:
                        for j in range(len(history)):
                            tf.write("{}\n".format(spu.toStr(history[j])))

                # Write statistics
                if statsFileName is not None:
                    with open(statsFileName, "a", encoding="utf-8") as sf:
                        sf.write("{},{},{:0.17f},{:0.0f},{:0.0f},{:0.0f}\n"\
                            .format(puzzle, spu.toStr(board), stats.executionTime, stats.unknowns, stats.guesses, stats.backtracks))
                
                i+=1

    except Exception as e:
        hasError = True
        spu.saveError(e, errorsFileName)