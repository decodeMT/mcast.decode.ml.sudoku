import backtracking as solvers
import sudokuPuzzleUtils as spu

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
    parser.add_argument("search", help="Defines how the puzzle is parsed: 1 by row; 2 by col; 3 by box sequentially; 4 by box in a zig-zag; 5 by box in a spiral; 6 by box in a semi-zig-zag.", type=int)
    parser.add_argument("guess", help="defines how numbers are guessed: 1 sequentially; 2 randomly.", type=int)

    args = parser.parse_args()
    solvers.solve(puzzlesFileName=args.puzzlesFileName, solutionsFileName=args.solutionsFileName, statsFileName=args.statsFileName,\
        trackingFileName=args.trackingFileName, errorsFileName=args.errorsFileName, offset=args.offset, limit=args.limit, search=args.search, guess=args.guess)

if (__name__=="__main__"):
    main()