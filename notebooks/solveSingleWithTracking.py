import sudokuSolvers as solvers
import sudokuPuzzleUtils as spu
import argparse
import timeit

def main():
    # Register arguments
    parser = argparse.ArgumentParser();
    parser.add_argument("puzzle", help="The puzzle to solve.", type=str)
    parser.add_argument("tracking", help="The file name of the tracking for the sudoku solutions.", type=str)
    parser.add_argument("stats", help="The file name where to save the sudoku stats.", type=str)
    parser.add_argument("errors", help="The file name where to save the errors.", type=str)
    parser.add_argument("search", help="Defines how the puzzle is parsed: 1 by row; 2 by col; 3 by box sequentially; 4 by box in a zig-zag; 5 by box in a spiral; 6 by box in a semi-zig-zag.", type=int)
    parser.add_argument("guess", help="defines how numbers are guessed: 1 sequentially; 2 randomly.", type=int)

    args = parser.parse_args()
    config = spu.SudokuConfig(searchMode=args.search, guessMode=args.guess, tracking=True)

    hasError=False
    try:
        print("Starting sudoku solver.")
        
        history = []
        board = spu.to2DArray(args.puzzle)

        config = spu.SudokuConfig(guessMode=args.guess, searchMode=args.search, tracking=True)
        stats = spu.SudokuStats()
        stats.setUnknowns(args.puzzle.count('0'))

        stats.registerExecutionTime(timeit.timeit(lambda: solvers.backtracking(board, history, stats, config), number=1000))                   

        # Write tracking
        with open(args.tracking, "w", encoding="utf-8") as sf:
            for i in range(len(history)):
                sf.write("{}\n".format(history[i]))

        # Write statistics
        with open(args.stats, "w", encoding="utf-8") as sf:
            sf.write("Puzzle,Solution,Execution Time,Zeros,Guesses,Backtracks\n")
            sf.write("{},{},{:0.17f},{:0.0f},{:0.0f},{:0.0f}\n"\
                .format(args.puzzle, spu.toStr(board), stats.executionTime, stats.unknowns, stats.guesses, stats.backtracks))
    except Exception as e:
        hasError = True
        spu.saveError(e, args.errors)

    print("Operation encountered some errors. Check {} for details or script output above.".format(args.errors) \
        if hasError else "Sudoku puzzles solved completed successfully.")
    print("Sudoku solver statistics saved in {}".format(args.stats))

if (__name__=="__main__"):
    main()