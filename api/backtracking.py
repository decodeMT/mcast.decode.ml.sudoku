import utils as utls


def findRandom(puzzle: list):
  """
  Finds the next empty cell in a random fashion.
  """
  import random

  for row in random.sample(range(0, 9), 9):
    for col in random.sample(range(0, 9), 9):
      if puzzle[row][col] == 0:
        return (row, col)

  return None


def findByRow(puzzle: list):
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


def findByCol(puzzle: list):
  """
  Finds the next empty cell in a column order.
  Arguments:
    puzzle: a 9x9 sudoku puzzle
  """
  for col in range(0, 9):
    for row in range(len(puzzle)):
      if puzzle[row][col] == 0:
        return (row, col)

  return None


def findByBox(puzzle: list, mode: int):
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

  if mode == 4:
    boxes = range(0, 9)
  elif mode == 5:
    boxes = [0, 1, 2, 5, 4, 3, 6, 7, 8]
  elif mode == 6:
    boxes = [0, 1, 2, 5, 8, 7, 6, 3, 4]
  elif mode == 7:
    boxes = [0, 1, 4, 3, 6, 7, 8, 5, 2]
  elif mode == 8:
    boxes = random.sample(range(0, 9), 9)
  elif mode == 9:
    boxes = [0, 4, 8, 1, 2, 3, 5, 6, 7]

  for box in boxes:
    for row in range((box // 3) * 3, ((box // 3) * 3) + 3):
      for col in range((box % 3) * 3, ((box % 3) * 3) + 3):
        if puzzle[row][col] == 0:
          return (row, col)

  return None


def findEmpty(puzzle: list, searchMode: int):
  """
  Finds the next empty cell in a 9x9 sudoku puzzle.
  Arguments:
    puzzle: the 9x9 sudoku puzzle.
    searchMode: defines how the puzzle is parsed: 
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
  if searchMode == 1:
    return findByRow(puzzle)
  elif searchMode == 2:
    return findByCol(puzzle)
  elif searchMode == 3:
    return findRandom(puzzle)
  elif searchMode >= 4 and searchMode <= 9:
    return findByBox(puzzle, searchMode)

  return None


def getGuesses(puzzle: list, guessMode: int):
  """
  Gets numbers to guess.
  Arguments:
    puzzle: the 9x9 sudoku puzzle.
    guessMode: the guessing mode. 1 for sequential, 2 for random.
  """
  import random

  if guessMode == 1:
    return range(1, 10)
  elif guessMode == 2:
    return random.sample(range(1, 10), 9)

  return None


def backtracking(board: list, stats: utls.SudokuStats,
                 config: utls.SudokuConfig):
  """
  Solves a 9x9 sudoku puzzle using backtracking algorithm.
  Arguments:
    board: the 9x9 puzzle to be solved.
    stats: The statistics object to record algorithm.
    searchMode: defines how the puzzle is parsed: 
      1 by row; 
      2 by col; 
      3 by box sequentially; 
      4 by box in a zig-zag; 
      5 by box in a spiral; 
      6 by box in a semi-zig-zag
    guessMode: defines how numbers are guessed: 1 sequentially; 2 randomly
  """
  # Find the next empty cell
  find = findEmpty(board, config.searchMode)

  # If there is no empty cell than puzzle is complete
  if not find:
    return True
  else:
    row, col = find

  # Get numbers to guess and attempt
  for guess in getGuesses(board, config.guessMode):
    if utls.isValid(board, guess, (row, col)):

      # Brute force guess
      stats.incrementGuesses()
      board[row][col] = guess

      stats.appendSolution(utls.toStr(board))

      # Attempt to solve rest of puzzle with current choice
      if backtracking(board, stats, config):
        return True

      # Invalid puzzle so backtrack
      stats.removeSolution(utls.toStr(board))
      stats.incrementBacktracks()
      board[row][col] = 0

  return False
