"""
Sudoku solver algorithms.

Author: Frankie Inguanez
Date: 27/01/2023
"""
import backtracking as bkSolver
import rulebased as rbSolver
import sudokuPuzzleUtils as spu

def getSearchAlg(searchMode: int) -> str:
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

def getGuessAlg(guessMode: int) -> str:
    """
    Translates a numeric guess mode to text.
    Arguments:
        guessMode: the numeric identifier for the guess mode.
    """
    if (guessMode==1):
        return "Sequential"
    elif (guessMode==2):
        return "Random"
    else: return "Unknown"

def getAlg(alg: int) -> str:
    """
    Translates a numeric algorithm to text.
    Arguments:
        alg: the algorithm identification number.
    """
    if alg==1:
        return "Backtracking"
    elif alg==2:
        return "Rules"
    else: return "Unknown"

def solve(  puzzlesFileName: str, solutionsFileName: str, statsFileName: str, trackingFileName: str, errorsFileName: str, \
            offset: int, limit: int, alg: int, searchMode: int, guessMode: int):
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
        alg: identifier for solution algorithm.
        searchMode: defines how missing values are searched.
        guessMode: defines how guesses are made.
    """
    import tqdm
    import timeit

    if not limit:
        limit = spu.getFileLineCount(puzzlesFileName)
    else: limit = limit

    i = 1
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
                if alg==1:
                    stats.registerExecutionTime(timeit.timeit(lambda: bkSolver.solve(board, validValues, history, stats, searchMode, guessMode), number=1000))
                elif alg==2:
                    stats.registerExecutionTime(timeit.timeit(lambda: rbSolver.solve(board, validValues, history, stats, searchMode, guessMode), number=1000))
                else: raise ValueError("Unrecognized algorithm identifier: {}\n".format(alg))
                
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
        spu.saveError(e, errorsFileName)

def main():
    import argparse

    # Register arguments
    parser = argparse.ArgumentParser();
    parser.add_argument("puzzlesFileName", help="The file name of the sudoku puzzles dataset.", type=str)
    parser.add_argument("solutionsFileName", help="The file name where to save the sudoku solutions.", type=str)
    parser.add_argument("statsFileName", help="The file name where to save the sudoku stats.", type=str)
    parser.add_argument("trackingFileName", help="The file name of the tracking for the sudoku solutions.", type=str) 
    parser.add_argument("errorsFileName", help="The file name where to save the errors.", type=str)
    parser.add_argument("offset", help="The number of puzzles to offset from the file.", type=int)
    parser.add_argument("limit", help="The limit number of puzzles to solve.", type=int)
    parser.add_argument("alg", help="The algorithm identifier.", type=int)
    parser.add_argument("search", help="Defines how the puzzle is parsed: 1 by row; 2 by col; 3 by box sequentially; 4 by box in a zig-zag; 5 by box in a spiral; 6 by box in a semi-zig-zag.", type=int)
    parser.add_argument("guess", help="defines how numbers are guessed: 1 sequentially; 2 randomly.", type=int)

    args = parser.parse_args()
    solve(puzzlesFileName=args.puzzlesFileName, solutionsFileName=args.solutionsFileName, statsFileName=args.statsFileName, \
        trackingFileName=args.trackingFileName, errorsFileName=args.errorsFileName, offset=args.offset, limit=args.limit, \
            alg=args.alg, searchMode=args.search, guessMode=args.guess)

if (__name__=="__main__"):
    main()