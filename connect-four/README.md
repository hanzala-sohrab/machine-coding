# Connect Four

A two-player Connect Four game built in Java. Players take turns dropping discs into a 7-column, 6-row board. The first to align four discs vertically, horizontally, or diagonally wins.

## How to Run

```bash
javac src/models/*.java
java -cp src models.Main
```

## Project Structure

```
src/models/
├── Main.java     # Entry point — game loop & board rendering
├── Game.java     # Game logic, turn management, win/draw detection
├── Board.java    # 6×7 grid, disc placement, four-in-a-row checks
└── Player.java   # Player name & color
```

## Gameplay

- Player 1 plays as **X**, Player 2 plays as **O**.
- On each turn, enter a column number (0–6) to drop a disc.
- The game announces the winner or a draw when the board is full.
