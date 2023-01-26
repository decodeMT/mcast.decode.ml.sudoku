"""
Sudoku Puzzle generator

Author: Frankie Inguanez
Date: 16/01/2023

A sudoku puzzle generator.
"""
import tqdm
import random
import sudokuPuzzleUtils as spu
import backtracking as solver

def generatePuzzles(count: int, minZeros: int, maxZeros:int, fileName: str):
    """
    Generates a number of 9x9 sudoku puzzle grid with a pre-defined number of zeros (unknowns).
    Arguments:
        count: the number of puzzles to generate.
        minZeros: the minimum number of zeros desired in each puzzle.
        maxZeros: the maximum number of zeros desired in each puzzle.
        fileName: the file name where to save the puzzles
    """

    try:
        with open(fileName, "w", encoding="utf-8") as f:
            print("Generating balanced dataset of {:0.0f} puzzles with {:0.0f} to {:0.0f} zeros.".format(count*(maxZeros+1-minZeros), minZeros, maxZeros))

            puzzles = {}
            # Loop for range of zeros
            for j in tqdm.tqdm(range(minZeros, maxZeros+1)):
                # Loop for number of puzzles per zeros
                for i in range(count):
                    # Create empty puzzle
                    board = spu.to2DArray('000000000000000000000000000000000000000000000000000000000000000000000000000000000')

                    # Solve puzzle
                    solver.backtracking(board=board, history=None, stats=None, searchMode=9, guessMode=2)

                    # Remove digits
                    changed = 0
                    while changed < j:
                        row = random.sample(range(0,9),1)[0]
                        col = random.sample(range(0,9),1)[0]
                        
                        if board[row][col]==0:
                            continue

                        board[row][col]=0
                        changed+=1

                    # Check if the puzzle was already created  
                    if puzzles.__contains__(spu.toStr(board)):
                        i-=1
                        continue
                    else:
                        puzzles[spu.toStr(board)]=board

                    # Write the puzzle
                    f.write("{}\n".format(spu.toStr(board)))

        print("Process completed successfully. Puzzles saved in {}\n".format(fileName))
    except Exception as e:
        print("Process failed due to:\n{}\n{}\n{}\n\n".format(type(e), e.args, e))


def main():
    import argparse

    # Register arguments
    parser = argparse.ArgumentParser();
    parser.add_argument("count", help="The number of puzzles to generate.", type=int)
    parser.add_argument("minZeros", help="The minimum number of zeros have in the puzzles.", type=int)
    parser.add_argument("maxZeros", help="The maximum number of zeros have in the puzzles.", type=int)
    parser.add_argument("fileName", help="The filename where to save the puzzles.", type=str)

    args = parser.parse_args()

    generatePuzzles(count=args.count, minZeros=args.minZeros, maxZeros=args.maxZeros, fileName=args.fileName)

if (__name__=="__main__"):
    main()