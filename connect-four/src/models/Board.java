package models;

enum Color {
  RED,
  YELLOW
}

class Board {
  private int rows;
  private int columns;
  private int[][] board;
  private int winningCount;

  Board(int r, int c) {
    rows = r;
    columns = c;
    winningCount = 4;
    board = new int[r][c];
  }

  public int getRows() {
    return rows;
  }

  public int getColumns() {
    return columns;
  }

  boolean isFull() {
    for (int i = 0; i < rows; ++i) {
      for (int j = 0; j < columns; ++j) {
        if (board[i][j] == 0) {
          return false;
        }
      }
    }
    return true;
  }

  boolean canPlace(int column) {
    if (column < 0 || column >= columns) {
      return false;
    }
    return board[rows - 1][column] == 0;
  }

  int place(int column, int color) {
    if (!canPlace(column)) {
      throw new IllegalArgumentException("Column is full");
    }

    for (int r = 0; r < rows; ++r) {
      if (board[r][column] == 0) {
        board[r][column] = color;
        return r;
      }
    }

    return -1;
  }

  boolean checkWin(int row, int column, int color) {
    int count = 0;
    for (int c = column; c < columns; c++) {
      if (board[row][c] == color) {
        ++count;
        if (count == winningCount) {
          return true;
        }
      } else {
        break;
      }
    }

    count = 0;
    for (int c = column; c >= 0; --c) {
      if (board[row][c] == color) {
        ++count;
        if (count == winningCount) {
          return true;
        }
      } else {
        break;
      }
    }

    count = 0;
    for (int r = row; r < rows; r++) {
      if (board[r][column] == color) {
        ++count;
        if (count == winningCount) {
          return true;
        }
      } else {
        break;
      }
    }

    count = 0;
    for (int r = row; r >= 0; --r) {
      if (board[r][column] == color) {
        ++count;
        if (count == winningCount) {
          return true;
        }
      } else {
        break;
      }
    }

    count = 0;
    for (int r = row, c = column; r < rows && c < columns; r++, c++) {
      if (board[r][c] == color) {
        ++count;
        if (count == winningCount) {
          return true;
        }
      } else {
        break;
      }
    }

    count = 0;
    for (int r = row, c = column; r < rows && c >= 0; r++, c--) {
      if (board[r][c] == color) {
        ++count;
        if (count == winningCount) {
          return true;
        }
      } else {
        break;
      }
    }

    count = 0;
    for (int r = row, c = column; r >= 0 && c < columns; r--, c++) {
      if (board[r][c] == color) {
        ++count;
        if (count == winningCount) {
          return true;
        }
      } else {
        break;
      }
    }

    count = 0;
    for (int r = row, c = column; r >= 0 && c >= 0; r--, c--) {
      if (board[r][c] == color) {
        ++count;
        if (count == winningCount) {
          return true;
        }
      } else {
        break;
      }
    }

    return false;
  }

  int getCell(int row, int column) {
    return board[row][column];
  }

  void setCell(int row, int column, int value) {
    board[row][column] = value;
  }
}
