package models;

enum GameState {
  WON,
  DRAW,
  IN_PROGRESS
}

class Game {
  private Board board;
  private Player player1;
  private Player player2;
  private Player currentPlayer;
  private Player winner;
  private GameState state;

  Game(Player p1, Player p2) {
    board = new Board(6, 7);
    player1 = p1;
    player2 = p2;
    currentPlayer = p1;
    winner = null;
    state = GameState.IN_PROGRESS;
  }

  void makeMove(Player p, int column) {
    // Validations
    if (p != currentPlayer) {
      throw new IllegalArgumentException("Not your turn");
    }
    if (board.isFull()) {
      state = GameState.DRAW;
      throw new IllegalArgumentException("Board is full");
    }
    if (!board.canPlace(column)) {
      throw new IllegalArgumentException("Column is full");
    }

    // Place the disc
    int r = board.place(column, p.getColor());

    if (r == -1) {
      throw new IllegalArgumentException("Column is full");
    }

    // Check if the current player has won
    if (board.checkWin(r, column, p.getColor())) {
      state = GameState.WON;
      winner = p;
      return;
    }

    // Change the player
    currentPlayer = currentPlayer == player1 ? player2 : player1; 
  }

  Player getCurrentPlayer() {
    return currentPlayer;
  }

  GameState getGameState() {
    return state;
  }

  Player getWinner() {
    return winner;
  }

  Board getBoard() {
    return board;
  }
}
