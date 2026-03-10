package models;

import java.util.Scanner;

public class Main {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);

    Player player1 = new Player("Player 1", 1);
    Player player2 = new Player("Player 2", 2);
    Game game = new Game(player1, player2);

    System.out.println("=== Connect Four ===");
    System.out.println(player1.getName() + " (X)  vs  " + player2.getName() + " (O)");
    System.out.println();

    while (game.getGameState() == GameState.IN_PROGRESS) {
      printBoard(game.getBoard());
      System.out.println(game.getCurrentPlayer().getName() + "'s turn.");
      System.out.print("Enter column (0-6): ");

      int column;
      try {
        column = Integer.parseInt(scanner.nextLine().trim());
      } catch (NumberFormatException e) {
        System.out.println("Invalid input. Please enter a number between 0 and 6.");
        continue;
      }

      try {
        game.makeMove(game.getCurrentPlayer(), column);
      } catch (IllegalArgumentException e) {
        System.out.println(e.getMessage());
      }
    }

    printBoard(game.getBoard());

    if (game.getGameState() == GameState.WON) {
      System.out.println("🎉 " + game.getWinner().getName() + " wins!");
    } else {
      System.out.println("It's a draw!");
    }

    scanner.close();
  }

  private static void printBoard(Board board) {
    // Print column numbers
    for (int c = 0; c < board.getColumns(); c++) {
      System.out.print("  " + c + " ");
    }
    System.out.println();

    // Print board (top row = highest index)
    for (int r = board.getRows() - 1; r >= 0; r--) {
      System.out.print("|");
      for (int c = 0; c < board.getColumns(); c++) {
        int cell = board.getCell(r, c);
        String symbol = cell == 0 ? " " : (cell == 1 ? "X" : "O");
        System.out.print(" " + symbol + " |");
      }
      System.out.println();
    }

    // Print bottom border
    for (int c = 0; c < board.getColumns(); c++) {
      System.out.print("----");
    }
    System.out.println("-");
    System.out.println();
  }
}
