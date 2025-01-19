# Minesweeper Game

## Description

This project is a Python implementation of the classic Minesweeper game with a customizable grid size, number of bombs, and an intuitive graphical user interface built using Tkinter. The game includes the ability to flag tiles, dynamically reveal empty tiles, and handles win/lose conditions.

## Features

- Customizable grid size and bomb percentage.
- Right-click to place/remove flags on tiles.
- Automatically reveals all connected empty tiles when a tile with no surrounding mines is clicked.
- End game handling with a "Game Over" or "You Win" message.
- Scrollable game area for large grids.
- Fullscreen toggle functionality.

## Project Structure

```
.
|-- src
|   |-- screen.py    # Main script for game logic and GUI
|   |-- tile.py      # Tile class defining the properties and behavior of each tile
|-- requirements.txt # Required Python libraries
```

## Installation

1. Clone this repository or download the files.
   ```
   git clone https://github.com/anthonyP1202/Another_Minesweeper.git
   ```
2. Install [Python](https://www.python.org/downloads/) (version 3.6 or later).
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the game by executing the `minesweeper.py` file:
   ```bash
   python src/screen.py
   ```
2. Adjust the grid size and bomb percentage using the input fields.
3. Click "Démarrer une partie" to start a new game.
4. Use the left mouse button to reveal a tile and the right mouse button to place/remove flags.

## Controls

- **Left-Click**: Reveal a tile.
- **Right-Click**: Place/remove a flag.
- **Space**: Toggle fullscreen mode. (! if u change the screen size Start a new game after , the board will be scalled with the screen)

## Gameplay Rules

- If you click on a bomb tile, the game ends with "Game Over."
- If you reveal all non-bomb tiles, you win the game.
- Flags are used to mark suspected bomb locations.
- Clicking on a tile with surrounding mines show you the number of mines around it.

![](docs\Exampleminesweeper1.png)

- Clicking on a tile with no surrounding mines automatically reveals all connected empty tiles.

![](docs\Exampleminesweeper2.png)

## Configuration

- **Grid Size**: Adjust the number of rows and columns using the "X (lines)" and "Y (columns)" fields.
- **Bomb Percentage**: Set the percentage of tiles that will contain bombs using the "Pourcentage de mines" field.

## File Overview

### `tile.py`

Defines the `Tile` class, which encapsulates the properties and behavior of individual tiles on the board:

- `is_mine`: Boolean indicating whether the tile is a mine.
- `location`: Coordinates of the tile.
- `surrounding_mine`: Number of mines surrounding this tile.
- `is_flagged`: Boolean indicating whether the tile is flagged.
- `surrounding_mines(board, away)`: Calculates the number of mines surrounding the tile.
- `surrounding_flags(board, away)`: Verifies if the number of flags around a tile matches the number of surrounding mines.

### `screen.py`

Implements the main game logic and GUI:

- **Functions**:
  - `create_board()`: Initializes the game board.
  - `calculate_bomb_count(board, percentage)`: Calculates the number of bombs based on the specified percentage.
  - `random_bomb_location(table, numb_bomb)`: Places bombs randomly on the board.
  - `reveal_tile(tile, button)`: Reveals the clicked tile and handles connected empty tiles.
  - `toggle_flag(tile, button)`: Places or removes a flag on a tile.
  - `check_win_condition()`: Checks if all non-bomb tiles have been revealed.
  - `end_game()`: Handles the game-over state.
  - `render_game_board(board)`: Renders the game board with buttons for each tile.
  - `start_game()`: Starts a new game.

### `requirements.txt`

Specifies the required libraries:

```
pygame
numpy
```

## Example

- Grid Size: 10x10
- Bomb Percentage: 15%

![](docs\Exampleminesweeper3.png)
![](docs\Exampleminesweeper4.png)

## Acknowledgments

This project was developed as part of a school project to demonstrate Python programming skills and GUI development using Tkinter.

## Authors

 
[Perreira Anthony](https://github.com/anthonyP1202) & [Vassy Mathis](https://github.com/VeldrX)

