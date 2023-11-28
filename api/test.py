import sudokuUtils as spu
import backtrackingSolver as bk
import ruleBasedSolver as rb
import json

def main():
    puzzle = "290684730048370509107002048051046072782093104060127080070465013416030857520718496"
    alg=1
    searchMode = 1 
    guessMode = 1

    board = spu.to2DArray(puzzle)

    board = spu.to2DArray(puzzle)

    history = list()
    stats = spu.SudokuStats()
    stats.setUnknowns(puzzle.count('0'))
    validValues = spu.cacheValidValues(board)
    if alg == 1:
        bk.solve(board, validValues, history, stats, searchMode, guessMode)
    elif alg == 2:
        rb.solve(board, validValues, history, stats, searchMode, guessMode)

    result = {
    "puzzle": puzzle,
    "zeros": stats.unknowns,
    "guesses": stats.guesses,
    "backtracks": stats.backtracks,
    "solutions": history
    }

    print(json.dumps(result))

if __name__ == "__main__":
    main()