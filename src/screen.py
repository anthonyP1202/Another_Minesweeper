import tkinter
from tkinter import ttk
import random
from tile import Tile
from collections import deque
import random


"""**************************************************************************************************************"""
"""****************************************                   ***************************************************"""
"""****************************************  Board Creation   ***************************************************"""
"""****************************************                   ***************************************************"""
"""**************************************************************************************************************"""

"""-----------------------------------------------"""
"""---------- Create the board of Tiles ----------"""
"""-----------------------------------------------"""


def create_board():
    x = 10
    y = 10

    try:
        x = int(size_x.get())
        y = int(size_y.get())
    except ValueError:
        pass

    board = []
    for cs in range(x):
        row = []
        for i in range(y):
            frame = Tile(location=[cs, i])  # Create a tile with coordinates
            row.append(frame)
        board.append(row)
    return board


"""---------------------------------------------------------------------------------------------"""
"""---------- Calculates the number of bombs based on a percentage of the total tiles ----------"""
"""---------------------------------------------------------------------------------------------"""


def calculate_bomb_count(board, percentage=15):

    percentage = float(percentage.get()) / 100
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    total_tiles = rows * cols
    return max(1, int(total_tiles * percentage))  # At least 1 bomb


"""-----------------------------------------------------------"""
"""---------- Place the bombs randomly on the board ----------"""
"""-----------------------------------------------------------"""


def random_bomb_location(table, numb_bomb):
    rows = len(table)
    cols = len(table[0]) if rows > 0 else 0
    total_tiles = rows * cols

    if numb_bomb > total_tiles:
        raise ValueError("Number of bombs cannot exceed the total number of tiles.")

    # Generate a list of all possible tile indices
    all_positions = [(r, c) for r in range(rows) for c in range(cols)]

    # Randomly sample numb_bomb unique positions
    bomb_positions = random.sample(all_positions, numb_bomb)

    # Place bombs on the randomly selected positions
    for row, col in bomb_positions:
        table[row][col].is_mine = True

    return table


"""--------------------------------------------------------------------"""
"""---------- Assign surrounding mines number for each tiles ----------"""
"""--------------------------------------------------------------------"""


def all_surrounding_mines(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j].surrounding_mines(board)  # Update the surrounding mines for each tile
    return board


"""*****************************************************************************************************************"""
"""****************************************                      ***************************************************"""
"""****************************************  Board Interaction   ***************************************************"""
"""****************************************                      ***************************************************"""
"""*****************************************************************************************************************"""


"""-----------------------------------------"""
"""---------- Toggle Flag on tile ----------"""
"""-----------------------------------------"""


def toggle_flag(tile, button):

    if tile in clicked_tiles:  # Check if the tile is already reaveled
        print("Tile is already revealed. Cannot place a flag.")
        return

    if not tile.is_flagged:  # add the flag
        tile.is_flagged = True
        button.config(text="🚩", state="normal")  # Mettre l'emoji du drapeau
    else:  # delete the flag
        tile.is_flagged = False
        button.config(text="", state="normal")


"""--------------------------------------"""
"""---------- Reveal the tiles ----------"""
"""--------------------------------------"""


def reveal_tile(tile, button):

    print(f"Clicked on tile at {tile.location}, is_mine: {tile.is_mine}, surrounding_mine: {tile.surrounding_mine}")

    if tile.is_flagged:  # Skip flagged tiles
        print("Tile is flagged, skipping.")
        return

    if tile.is_mine:  # Game over on clicking a mine
        button.config(text="💣", bg="red")
        game_over()
        return

    if tile in clicked_tiles:
        x, y = tile.location
        print("in clicked")
        if tile.surrounding_flags(test_board) == True:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue  # Skip the tile itself

                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(test_board) and 0 <= ny < len(test_board[0]):
                        neighbor = test_board[nx][ny]
                        button = buttons[nx * len(test_board[0]) + ny]  # Find the button for this tile
                        if neighbor not in clicked_tiles:
                            reveal_tile(neighbor, button)

    if tile not in clicked_tiles:
        # First click: reveal the tile
        clicked_tiles.add(tile)
        button.config(
            text=str(tile.surrounding_mine) if tile.surrounding_mine > 0 else "",
            relief="sunken",
            bg="lightgrey" if tile.surrounding_mine == 0 else "SystemButtonFace",
        )
        if tile.surrounding_mine == 0:
            reveal_connected_tiles(tile)
    check_win_condition()


"""-------------------------------------------------------------------"""
"""---------- Iteratively reveals all connected empty tiles ----------"""
"""-------------------------------------------------------------------"""


def reveal_connected_tiles(tile):

    # Initialize a queue with the starting tile
    queue = deque([tile])
    clicked_tiles.add(tile)

    # List to store tiles that need to be updated
    tiles_to_update = []

    while queue:
        current_tile = queue.popleft()  # Pop the next tile to reveal
        x, y = current_tile.location
        tiles_to_update.append(current_tile)  # Add to update list

        # If the current tile is empty (surrounding_mine == 0), we add its neighbors to the queue
        if current_tile.surrounding_mine == 0:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue  # Skip the tile itself

                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(test_board) and 0 <= ny < len(test_board[0]):
                        neighbor = test_board[nx][ny]
                        if neighbor not in clicked_tiles:  # Add unclicked neighbors
                            clicked_tiles.add(neighbor)
                            queue.append(neighbor)

    # Now, update all tiles in batch (after collecting all connected tiles)
    for current_tile in tiles_to_update:
        x, y = current_tile.location
        button = buttons[x * len(test_board[0]) + y]  # Find the button for this tile

        # Update button text and background
        button.config(
            text=str(current_tile.surrounding_mine) if current_tile.surrounding_mine > 0 else "",
            bg="lightgrey" if current_tile.surrounding_mine == 0 else "SystemButtonFace",
            relief="sunken",
        )
    check_win_condition()


"""***********************************************************************************************************"""
"""****************************************                ***************************************************"""
"""****************************************  Game Screen   ***************************************************"""
"""****************************************                ***************************************************"""
"""***********************************************************************************************************"""


"""-------------------------------------------------------------------------------------"""
"""---------- Displays the game board with buttons corresponding to the tiles ----------"""
"""-------------------------------------------------------------------------------------"""


def render_game_board(board):
    global buttons
    buttons = []  # Reset the button list

    # Create a style for the scrollbars
    style = tkinter.ttk.Style()
    style.theme_use("default")  # Use default theme for customization
    style.configure("Red.Vertical.TScrollbar", background="red", troughcolor="white", arrowcolor="red")
    style.configure("Red.Horizontal.TScrollbar", background="red", troughcolor="white", arrowcolor="red")

    # Create the canvas and scrollbars
    # Create the canvas and scrollbars
    canvas = tkinter.Canvas(game_frame)
    scrollbar_y = tkinter.ttk.Scrollbar(
        game_frame, orient="vertical", command=canvas.yview, style="Red.Vertical.TScrollbar"
    )
    scrollbar_x = tkinter.ttk.Scrollbar(
        game_frame, orient="horizontal", command=canvas.xview, style="Red.Horizontal.TScrollbar"
    )
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Create a frame to hold the game board on the canvas
    board_frame = tkinter.Frame(canvas)

    # Create the buttons and add them to the board frame
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            # Create a button for each tile
            btn = tkinter.Button(board_frame, width=3, height=1, text="")
            btn.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")  # Make the button expand

            # Associate left and right clicks
            btn.config(command=lambda t=tile, b=btn: reveal_tile(t, b))  # Left click
            btn.bind("<Button-3>", lambda event, t=tile, b=btn: toggle_flag(t, b))  # Right click

            # Add the button to the list
            buttons.append(btn)

    # Dynamically scale rows and columns
    for i in range(len(board)):
        board_frame.grid_rowconfigure(i, weight=1, minsize=40)  # Scale row to expand
    for j in range(len(board[0])):
        board_frame.grid_columnconfigure(j, weight=1, minsize=40)  # Scale column to expand

    # Add the frame to the canvas and scrollbars to the window
    canvas.create_window((0, 0), window=board_frame, anchor="nw")

    # Dynamically resize the canvas and its frame based on the window size
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    # Update the scrollable region after rendering the game board
    board_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))  # Adjust scrollable region

    # Dynamically resize grid to fit the board's size, but make the game_frame a little smaller than the window
    game_frame.grid_rowconfigure(0, weight=1)
    game_frame.grid_columnconfigure(0, weight=1)
    game_frame.place(
        relx=0.5, rely=0.6, anchor="center", width=root.winfo_width() * 0.9, height=root.winfo_height() * 0.7
    )


"""----------------------------------"""
"""---------- Start a game ----------"""
"""----------------------------------"""


def start_game():

    global test_board, clicked_tiles
    clicked_tiles = set()  # Reset clicked tiles

    # Create a new game board
    test_board = create_board()
    num_bombs = calculate_bomb_count(test_board, Bomb_percent)  # 15% of tiles are bombs
    test_board = random_bomb_location(test_board, num_bombs)
    test_board = all_surrounding_mines(test_board)

    is_mine_matrix = [[tile.is_mine for tile in row] for row in test_board]

    # Print the matrix
    for row in is_mine_matrix:
        print(row)

    count = 0
    for n in test_board:
        for k in n:
            if k.is_mine:
                count += 1
    print(count)

    # Clear the game area and render the new board
    for widget in game_frame.winfo_children():
        widget.destroy()

    render_game_board(test_board)


"""------------------------------------"""
"""---------- Win Conditions ----------"""
"""------------------------------------"""


def check_win_condition():

    non_bomb_tiles = 0
    revealed_tiles = 0

    for row in test_board:
        for tile in row:
            if not tile.is_mine:
                non_bomb_tiles += 1
                if tile in clicked_tiles:
                    revealed_tiles += 1

    if revealed_tiles == non_bomb_tiles:
        # If all non-bomb tiles are revealed, display win message
        display_win_message()


"""-------------------------------"""
"""---------- Game Over ----------"""
"""-------------------------------"""


def game_over():

    for btn in buttons:
        btn.config(state="disabled")  # disable buttons

    # Game Over message
    game_over_label = tkinter.Label(root, text="GAME OVER", font=("Arial", 24), fg="red", bg="white")
    game_over_label.place(relx=0.5, rely=0.5, anchor="center")
    root.after(2000, game_over_label.destroy)


"""-------------------------------------------------------------------"""
"""---------- Displays win message and disables all buttons ----------"""
"""-------------------------------------------------------------------"""


def display_win_message():

    win_label = tkinter.Label(root, text="YOU WIN!", font=("Arial", 24), fg="green", bg="white")
    win_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the message
    root.after(2000, win_label.destroy)  # Remove the message after 2 seconds

    for btn in buttons:
        btn.config(state="disabled")  # Disable all buttons to prevent further clicks


"""*********************************************************************************************************"""
"""****************************************              ***************************************************"""
"""****************************************  Variables   ***************************************************"""
"""****************************************              ***************************************************"""
"""*********************************************************************************************************"""
# GUI setup
root = tkinter.Tk()

# Enable fullscreen initially
root.attributes("-fullscreen", True)


# Function to toggle fullscreen mode
def toggle_fullscreen(event=None):
    is_fullscreen = root.attributes("-fullscreen")
    root.attributes("-fullscreen", not is_fullscreen)


# Bind the Space key to exit fullscreen
root.bind("<space>", lambda event: root.attributes("-fullscreen", False))

# Bind the Space key to re-enter fullscreen
root.bind("<space>", toggle_fullscreen)

root.geometry("1600x900")


# Game zone (add a border around the game area)
game_frame = tkinter.Frame(root, bg="lightblue", borderwidth=10, relief="solid")  # Change the color here
game_frame.place(relx=0.5, rely=0.6, anchor="center")


size_frame = tkinter.Frame(root)  # Frame pour regrouper les entrées et les labels
size_frame.pack(pady=10)

# Label and field for size X
label_x = tkinter.Label(size_frame, text="X (lines) :")
label_x.grid(row=0, column=0, padx=5)
size_x = tkinter.Entry(size_frame, width=5)
size_x.insert(0, "10")  # Valeur par défaut
size_x.grid(row=0, column=1, padx=5)

# Label and field for size Y
label_y = tkinter.Label(size_frame, text="Y (columns) :")
label_y.grid(row=1, column=0, padx=5)
size_y = tkinter.Entry(size_frame, width=5)
size_y.insert(0, "10")  # Valeur par défaut
size_y.grid(row=1, column=1, padx=5)

# Label and field for mine percentage
label_percentage = tkinter.Label(size_frame, text="Percentage of mines :")
label_percentage.grid(row=2, column=0, padx=5)
Bomb_percent = tkinter.Entry(size_frame, width=10)
Bomb_percent.insert(0, "15")  # Valeur par défaut
Bomb_percent.grid(row=2, column=1, padx=5)

# Start Button
start_button = tkinter.Button(root, text="Start a Game", command=start_game)
start_button.pack(pady=10)

# Add the Quit button to the GUI
quit_button = tkinter.Button(root, text="Quit", command=root.quit)
quit_button.pack(pady=10)  # You can change the padding or position as needed


start_game()
root.mainloop()
