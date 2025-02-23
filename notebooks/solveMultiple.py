import sudokuSolvers as solvers
import sudokuPuzzleUtils as spu

def solvePuzzles(executor: spu.SudokuExecutor, config: spu.SudokuConfig):
    """
    Solves puzzles found in a file using backtracking algorithm.
    Arguments:
        puzzlesFileName: file containing puzzles in following format: <id>, <puzzle>, <solution>
        statsFileName: file where statistics shall be saved.
        errorsFileName: file where errors shall be saved.
        limit: the limit number of puzzles to solve.
        searchMode: defines how missing values are searched.
        guessMode: defines how guesses are made.
    """
    import tqdm
    import timeit

    if not executor.limit:
        limit = spu.getFileLineCount(executor.puzzlesFileName)
    else: limit = executor.limit

    i = 1
    hasError = False
    try:
        print("Starting sudoku base solver.")
        
        # Open statistics file
        with open(executor.statsFileName, "w", encoding="utf-8") as sf:
            #Write header row
            sf.write("Puzzle,Solution,Execution Time,Zeros,Guesses,Backtracks\n")

            # Open puzzles and read till limit is reached.
            with open(executor.puzzlesFileName, "r", encoding="utf-8") as pf:
                for line in tqdm.tqdm(pf, total=limit):
                    # Stop at limit
                    if (i>limit):
                        break

                    # Create board and statistics
                    puzzle=line.strip()
                    board = spu.to2DArray(puzzle)
                    
                    stats = spu.SudokuStats();
                    stats.setUnknowns(puzzle.count('0'))
                    stats.registerExecutionTime(timeit.timeit(lambda: solvers.backtracking(board, None, stats, config), number=1000))                   
                        
                    # Write statistics
                    sf.write("{},{},{:0.17f},{:0.0f},{:0.0f},{:0.0f}\n"\
                        .format(puzzle, spu.toStr(board), stats.executionTime, stats.unknowns, stats.guesses, stats.backtracks))
                    i+=1

    except Exception as e:
        hasError = True
        spu.saveError(e, executor.errorsFileName)

    print("Operation encountered some errors. Check {} for details or script output above.".format(executor.errorsFileName) \
        if hasError else "Sudoku puzzles solved completed successfully.")
    print("Sudoku solver statistics saved in {}".format(executor.statsFileName))

def main():
    import argparse

    # Register arguments
    parser = argparse.ArgumentParser();
    parser.add_argument("puzzles", help="The file name of the sudoku puzzles dataset.", type=str)
    parser.add_argument("stats", help="The file name where to save the sudoku stats.", type=str)
    parser.add_argument("errors", help="The file name where to save the errors.", type=str)
    parser.add_argument("offset", help="The number of puzzles to offset from the file.", type=int)
    parser.add_argument("limit", help="The limit number of puzzles to solve.", type=int)
    parser.add_argument("search", help="Defines how the puzzle is parsed: 1 by row; 2 by col; 3 by box sequentially; 4 by box in a zig-zag; 5 by box in a spiral; 6 by box in a semi-zig-zag.", type=int)
    parser.add_argument("guess", help="defines how numbers are guessed: 1 sequentially; 2 randomly.", type=int)

    args = parser.parse_args()
    config = spu.SudokuConfig(searchMode=args.search, guessMode=args.guess, tracking=False)
    exec = spu.SudokuExecutor(puzzlesFileName=args.puzzles, trackingFileName=None, statsFileName=args.stats, errorsFileName=args.errors, offset=args.offset, limit=args.limit)

    solvePuzzles(executor=exec, config=config)

if (__name__=="__main__"):
    main()