import tkinter
import random
from tile import Tile  # Assuming the Tile class is as defined above

# Function to create the board with Tile objects
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

def calculate_bomb_count(board, percentage=0.15):
    """
    Calcule le nombre de bombes en fonction d'un pourcentage du total des tuiles.
    Par défaut, 15 % des tuiles sont des bombes.
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    total_tiles = rows * cols
    return max(1, int(total_tiles * percentage))  # Au moins 1 bombe

# Function to place bombs randomly on the board
def random_bomb_location(table, numb_bomb):
    trash = []
    rows = len(table)
    cols = len(table[0]) if rows > 0 else 0

    for _ in range(numb_bomb):
        rand_row = random.randint(0, rows - 1)
        rand_col = random.randint(0, cols - 1)
        if [rand_row, rand_col] in trash:
            continue  # Skip if the location already has a mine
        else:
            trash.append([rand_row, rand_col])
            table[rand_row][rand_col].is_mine = True  # Place a mine on the tile

    return table


# Function to calculate all surrounding mines for each tile
def all_surrounding_mines(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j].surrounding_mines(board)  # Update the surrounding mines for each tile
    return board


# Fonction pour ajouter ou retirer un drapeau
def toggle_flag(tile, button):
    """
    Place ou retire un drapeau sur le bouton correspondant à la tuile.
    """
    if not tile.is_flagged:  # Place un drapeau
        tile.is_flagged = True
        button.config(text="🚩", state="normal")  # Mettre l'emoji du drapeau
    else:  # Retire le drapeau
        tile.is_flagged = False
        button.config(text="", state="normal")  # Supprime l'emoji

# Fonction pour révéler une tuile (clic gauche)
def reveal_tile(tile, button):
    """
    Révèle la tuile (clic gauche). Si la tuile est une mine, elle termine le jeu.
    """
    if tile.is_flagged:  # Ne rien faire si un drapeau est placé
        return
    
    if tile.is_mine:
        button.config(text="💣", bg="red")  # Affiche une bombe
        print("Game Over!")  # Vous pouvez ajouter une logique pour terminer la partie
    else:
        button.config(text=str(tile.surrounding_mine) if tile.surrounding_mine > 0 else "",
                      state="disabled", relief="sunken")
        if tile.surrounding_mine == 0:
            button.config(bg="lightgrey")

# Fonction pour afficher le plateau de jeu
def render_game_board(board):
    """
    Affiche le plateau de jeu avec des boutons correspondant aux tuiles.
    """
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            # Créez un bouton pour chaque tuile
            btn = tkinter.Button(game_frame, width=3, height=1, text="")
            btn.grid(row=i, column=j, padx=1, pady=1)

            # Associer les clics gauche et droit
            btn.config(command=lambda t=tile, b=btn: reveal_tile(t, b))  # Clic gauche
            btn.bind("<Button-3>", lambda event, t=tile, b=btn: toggle_flag(t, b))  # Clic droit




# GUI setup
root = tkinter.Tk()
root.geometry("800x600")
root.title("Minesweeper")

# Entry for board size settings
size_x = tkinter.Entry(root, width=5)
size_x.insert(0, "10")
size_x.pack(side="left")

size_y = tkinter.Entry(root, width=5)
size_y.insert(0, "10")
size_y.pack(side="left")

# Start game button
start_button = tkinter.Button(root, text="Start Game", command=lambda: start_game())
start_button.pack(side="left")

# Frame for game area
game_frame = tkinter.Frame(root)
game_frame.pack(expand=True, fill="both")

# Function to start/restart the game
def start_game():
    for widget in game_frame.winfo_children():
        widget.destroy()  # Clear the game frame

    global test_board
    test_board = create_board()
    num_bombs = calculate_bomb_count(test_board, percentage=0.15)  # Ajustez le pourcentage si nécessaire
    test_board = random_bomb_location(test_board, num_bombs)  # Place 10 bombs
    test_board = all_surrounding_mines(test_board)  # Calculate surrounding mines
    render_game_board(test_board)  # Render the board as buttons


# Start the main loop
root.mainloop()
