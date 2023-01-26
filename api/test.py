import utils as utls
import backtracking as solver
import json

def main():
    puzzle = "290684730048370509107002048051046072782093104060127080070465013416030857520718496"
    search = "1" 
    guess = "1"

    board = utls.to2DArray(puzzle)
    stats = utls.SudokuStats()
    stats.setUnknowns(puzzle.count("0"))
    config = utls.SudokuConfig(searchMode=int(search), guessMode=int(guess))
    solver.backtracking(board=board, stats=stats, config=config)

    result = {
        "puzzle": puzzle,
        "zeros": stats.unknowns,
        "guesses": stats.guesses,
        "backtracks": stats.backtracks,
        "solutions": stats.history
    }

    print(json.dumps(result))

if __name__ == "__main__":
    main()