"""
Dataset evaluator

Author: Frankie Inguanez
Date: 26/01/2023
"""

import pandas as pd
import sudokuPuzzleUtils as spu
import sudokuSolver as solver

def evaluate(puzzlesFileName: str, outputDir: str, offset: int, limit: int):
    """
    Evaluates all implemented algorithms and variations, for a limit number of puzzles.
    Arguments:
        puzzlesFileName: the file name of the puzzles.
        outputDir: the directory where to store all output.
        offset: the number of puzzles to offset.
        limit: the limit number of puzzles to consider.
    """
    # Solve with all possible combinations and save statistics
    for s in range(1,10):
        for g in range(1,3):
            for a in range(1,3):
                solver.solve(puzzlesFileName=puzzlesFileName, solutionsFileName=str(None), statsFileName="{}/{}_search_{:0.0f}_guess_{:0.0f}.csv".format(outputDir, solver.getAlg(a), s, g),\
                    trackingFileName=str(None), errorsFileName="{}/backtrackingErrors.txt".format(outputDir), offset=offset, limit=limit, alg=a, searchMode=s, guessMode=g)

    # Read all generated files and merge
    stats = pd.DataFrame()

    for s in range(1,10):
        for g in range (1,3):
            for a in range(1,3):
                data = pd.read_csv("{}/{}_search_{:0.0f}_guess_{:0.0f}.csv".format(outputDir, solver.getAlg(a), s, g))

                data["algorithm"]=solver.getAlg(a)
                data["search"]=s
                data["guess"]=g

                if stats.__len__()== 0:
                    stats = data
                else:
                    stats = pd.concat((stats, data), axis=0)

    # Generate execution time and backtracking plots, then save each.
    for s in range(1,10):
        for a in range(1,3):
            toPlot = pd.DataFrame()
            toPlot["Zeros"] = stats[(stats["algorithm"]==solver.getAlg(a)) & (stats["search"]==s)].groupby(by="Zeros").count().index
            toPlot["Sequential"] = stats[(stats["algorithm"]==solver.getAlg(a)) & (stats["search"]==s) & (stats["guess"]==1)].groupby(by="Zeros")["Execution Time"].mean().values
            toPlot["Random"] = stats[(stats["algorithm"]==solver.getAlg(a)) & (stats["search"]==s) & (stats["guess"]==2)].groupby(by="Zeros")["Execution Time"].mean().values

            ax = toPlot.plot(x="Zeros", y=["Sequential", "Random"], kind="bar", rot=0, figsize=(10,6))
            ax.set_ylabel("Mean execution time")
            ax.set_title("{} - Search {} - Execution Analysis".format(solver.getAlg(a), solver.getSearchAlg(s)))
            ax.figure.savefig("{}/{}_search_{:0.0f}_execution_time.PNG".format(outputDir, solver.getAlg(a), s))
            ax.figure.clear()

            toPlot = pd.DataFrame()
            toPlot["Zeros"] = stats[(stats["algorithm"]==solver.getAlg(a)) & (stats["search"]==s)].groupby(by="Zeros").count().index
            toPlot["Sequential"] = stats[(stats["algorithm"]==solver.getAlg(a)) & (stats["search"]==s) & (stats["guess"]==1)].groupby(by="Zeros")["Backtracks"].mean().values
            toPlot["Random"] = stats[(stats["algorithm"]==solver.getAlg(a)) & (stats["search"]==s) & (stats["guess"]==2)].groupby(by="Zeros")["Backtracks"].mean().values

            ax = toPlot.plot(x="Zeros", y=["Sequential", "Random"], kind="bar", rot=0, figsize=(10,6))
            ax.set_ylabel("Mean Backtracks")
            ax.set_title("{} - Search {} - Backtracks Analysis".format(solver.getAlg(a), solver.getSearchAlg(s)))
            ax.figure.savefig("{}/{}_search_{:0.0f}_backtracks.PNG".format(outputDir, solver.getAlg(a), s))
            ax.figure.clear()

    # Generate and save all stats
    aggregatedStats = stats.groupby(by=["algorithm", "search", "guess", "Zeros"])\
                        .aggregate({"Execution Time": ["count", "min", "max", "mean",], "Guesses": ["min", "max", "mean"], "Backtracks": ["min", "max", "mean"]})
    aggregatedStats.to_csv("{}/prototype_analysis.csv".format(outputDir))

def main():
    import argparse

    # Register arguments
    parser = argparse.ArgumentParser();
    parser.add_argument("puzzlesFileName", help="The file name of the puzzles.", type=str)
    parser.add_argument("outputDir", help="The directory where to store the files.", type=str)
    parser.add_argument("offset", help="The number of puzzles to offset from the file.", type=int)
    parser.add_argument("limit", help="The max number of puzzles to consider.", type=int)
    args = parser.parse_args()

    evaluate(args.puzzlesFileName, args.outputDir, args.offset, args.limit)
    
if (__name__=="__main__"):
    main()