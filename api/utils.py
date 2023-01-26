class SudokuConfig:

  def __init__(self, searchMode: int, guessMode: int):
    self.searchMode = searchMode
    self.guessMode = guessMode


class SudokuStats:

  def __init__(self):
    self.guesses = 0
    self.backtracks = 0
    self.unknowns = 0
    self.history = []

  def incrementGuesses(self):
    self.guesses += 1

  def incrementBacktracks(self):
    self.backtracks += 1

  def setUnknowns(self, zeros: int):
    self.unknowns = zeros

  def appendSolution(self, solution: list):
    self.history.append(solution)

  def removeSolution(self, solution: list):
    self.history.remove(solution)


def to2DArray(n: str):
  """
  Convert a string to a 2D 9x9 array.
  Arguments:
      n: an 81 digits in string format.
  """
  return [list(map(int, n[i:i + 9])) for i in range(0, 81, 9)]


def toStr(puzzle: list):
  """
  Converts a puzzle to a string.
  Arguments:
      puzzle: a 2 dimensional array representing the 9x9 puzzle. 
  """
  r = ""

  for row in puzzle:
    r += "".join(map(str, row))

  return r


def getColValues(puzzle: list, col: int):
  """
  Get column values.
  Arguments:
    puzzle: a 2 dimensional array representing the 9x9 puzzle. 
    col: the column number.
  """
  lst = []
  for row in puzzle:
    lst.append(row[col])

  return lst


def getBoxValues(puzzle: list, box: int):
  """
  Get box values. Boxes are 3x3 sub-grids enumerates from top left in a raster fashion
  0, 1, 2
  3, 4, 5
  6, 7, 8
  Arguments:
      puzzle: a 2 dimensional array representing the 9x9 puzzle.
      box: the box identification number.
  """
  return [
    puzzle[x][y] for x in range((box // 3) * 3, ((box // 3) * 3) + 3)
    for y in range((box % 3) * 3, ((box % 3) * 3) + 3)
  ]


def checkList(lst: list):
  """
  Checks if a list contains all numbers from 1 to 9.
  Arguments:
      lst: the list of numbers.
  """
  return set(lst) == set(range(1, 10))


def isSolved(puzzle: list):
  """
  Check if a puzzle has been solved.
  Arguments:
      puzzle: a 2 dimensional array representing the 9x9 puzzle.
  """

  # Check rows
  for row in puzzle:
    if not checkList(row):
      return False

  # Check columns
  for i in range(0, 9):
    if not checkList(getColValues(puzzle, i)):
      return False

  # Check box
  for i in range(0, 9):
    if not checkList(getBoxValues(puzzle, i)):
      return False

  return True


def isValid(puzzle: list, num: int, pos):
  """
  Checks if a number can be added to a specific position
  Arguments:
    puzzle: a 2 dimensional array representing the 9x9 puzzle.
    num: the number to insert.
    pos: the row and column position to place the digit.
  """

  # Check the row
  for i in range(len(puzzle[0])):
    if puzzle[pos[0]][i] == num and pos[1] != i:
      return False

  # Check the column
  for i in range(len(puzzle[1])):
    if puzzle[i][pos[1]] == num and pos[0] != i:
      return False

  # Check box
  box_x = pos[1] // 3
  box_y = pos[0] // 3

  for i in range(box_y * 3, box_y * 3 + 3):
    for j in range(box_x * 3, box_x * 3 + 3):
      if puzzle[i][j] == num and (i, j) != pos:
        return False

  return True
