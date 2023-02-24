"""
Dataset evaluator

Author: Frankie Inguanez
Date: 26/01/2023
"""
import tqdm
import sudokuPuzzleUtils as spu
from matplotlib import pyplot as plt

def eval(puzzlesFileName: str, zerosFileName:str, difficultyFileName:str):
    """
    Evaluates a dataset, by generating histograms for number of zeros and difficulty level.
    Arguments:
        puzzlesFileName: the file name where the puzzles are located.
        zerosFileName: the file name where to save the histogram for number of zeros.
        difficultyFileName: the file name where to save the histogram for difficulty levels.
    """
    # Prepare the dictionary
    zeros = dict()
    for i in range(0,81):
        zeros[i] = 0

    # Read the puzzles file
    with open(puzzlesFileName, "r", encoding="utf-8") as pf:
        for line in tqdm.tqdm(pf, total=spu.getFileLineCount(puzzlesFileName)):
            # Count the number of zeros
            zeroCount = line.count('0')
            zeros[zeroCount] += 1     

    # Reduce dictionary to include only non zero keys
    stats = dict()
    for i in range(0,81):
        if zeros[i]==0:
            continue

        stats[i]=zeros[i]

    # Create histogram for number of zeros and save
    plt.figure(figsize=(10,6), dpi=150)
    plt.bar(range(len(stats)), list(stats.values()), align='center')
    plt.xticks(range(len(stats)), list(stats.keys()))
    plt.xlabel("Number of zeros")
    plt.ylabel("Puzzle count")
    plt.title("Dataset evaluation")
    plt.savefig(zerosFileName)
    plt.close()

    # Create buckets for level of difficulty
    buckets = {0:0, 1:0, 2:0, 3:0, 4:0}

    for i in list(stats.keys()):
        if (81-i)>46:
            buckets[0]+=stats[i]
        elif (81-i)>=36:
            buckets[1]+=stats[i]
        elif (81-i)>=32:
            buckets[2]+=stats[i]
        elif (81-i)>=28:
            buckets[3]+=stats[i]
        else: buckets[4]+=stats[i]

    # Create histogram for difficulty level and save
    plt.bar(range(len(buckets)), list(buckets.values()), align='center')
    plt.xticks(range(len(buckets)), list(buckets.keys()))
    plt.xlabel("Difficulty level")
    plt.ylabel("Puzzle count")
    plt.title("Dataset evaluation")
    plt.savefig(difficultyFileName)

def main():
    import argparse

    # Register arguments
    parser = argparse.ArgumentParser();
    parser.add_argument("puzzlesFileName", help="The file name of the puzzles.", type=str)
    parser.add_argument("zerosFileName", help="The file name for the zeros plot.", type=str)
    parser.add_argument("difficultyFileName", help="The file name for the difficulty level plot.", type=str)

    args = parser.parse_args()
    eval(args.puzzlesFileName, args.zerosFileName, args.difficultyFileName)

if (__name__=="__main__"):
    main()