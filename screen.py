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
# Variable pour stocker les boutons (facilite leur gestion)
buttons = []

# Fonction pour terminer le jeu
def end_game():
    """
    Affiche 'Game Over', désactive tous les boutons, et empêche toute interaction.
    """
    for btn in buttons:
        btn.config(state="disabled")  # Désactiver tous les boutons
    
    # Afficher un message Game Over
    game_over_label = tkinter.Label(root, text="GAME OVER", font=("Arial", 24), fg="red", bg="white")
    game_over_label.place(relx=0.5, rely=0.5, anchor="center")  # Centrer le message
    root.after(2000, game_over_label.destroy)  # Supprime le message après 2 secondes

# Fonction pour révéler une tuile (clic gauche)
clicked_tiles = set()

def reveal_tile(tile, button):
    """
    Reveals a tile. If clicked again on an already revealed empty tile (surrounding_mine == 0),
    reveals all connected empty tiles and their neighbors.
    """
    print(f"Clicked on tile at {tile.location}, is_mine: {tile.is_mine}, surrounding_mine: {tile.surrounding_mine}")
    
    if tile.is_flagged:  # Skip flagged tiles
        print("Tile is flagged, skipping.")
        return
    
    if tile.is_mine:  # Game over on clicking a mine
        button.config(text="💣", bg="red")
        end_game()
        return

    if tile not in clicked_tiles:
        # First click: reveal the tile
        clicked_tiles.add(tile)
        button.config(
            text=str(tile.surrounding_mine) if tile.surrounding_mine > 0 else "",
            relief="sunken",
            bg="lightgrey" if tile.surrounding_mine == 0 else "SystemButtonFace"
        )
    else:
        # Second click: reveal all connected empty tiles
        if tile.surrounding_mine == 0:
            print("Revealing connected tiles.")
            reveal_connected_tiles(tile)
    check_win_condition() 



def reveal_connected_tiles(tile):
    """
    Recursively reveals all connected empty tiles and their neighbors.
    """
    x, y = tile.location
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue  # Skip the tile itself
            
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(test_board) and 0 <= ny < len(test_board[0]):
                neighbor = test_board[nx][ny]
                button = buttons[nx * len(test_board[0]) + ny]  # Find the button for this tile
                if neighbor not in clicked_tiles:  # Reveal only if not already revealed
                    clicked_tiles.add(neighbor)
                    neighbor_button_text = str(neighbor.surrounding_mine) if neighbor.surrounding_mine > 0 else ""
                    neighbor_button_bg = "lightgrey" if neighbor.surrounding_mine == 0 else "SystemButtonFace"
                    button.config(text=neighbor_button_text, bg=neighbor_button_bg, state="disabled", relief="sunken")
                    if neighbor.surrounding_mine == 0:  # If neighbor is also empty, continue flood-fill
                        reveal_connected_tiles(neighbor)
    check_win_condition()


# Fonction pour afficher le plateau de jeu
def render_game_board(board):
    """
    Affiche le plateau de jeu avec des boutons correspondant aux tuiles.
    """
    global buttons
    buttons = []  # Réinitialiser la liste des boutons
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            # Créez un bouton pour chaque tuile
            btn = tkinter.Button(game_frame, width=3, height=1, text="")
            btn.grid(row=i, column=j, padx=1, pady=1)

            # Associer les clics gauche et droit
            btn.config(command=lambda t=tile, b=btn: reveal_tile(t, b))  # Clic gauche
            btn.bind("<Button-3>", lambda event, t=tile, b=btn: toggle_flag(t, b))  # Clic droit
            
            # Ajouter le bouton à la liste
            buttons.append(btn)

# Fonction pour démarrer une nouvelle partie
def start_game():
    """
    Starts a new game.
    """
    global test_board, clicked_tiles
    clicked_tiles = set()  # Reset clicked tiles

    # Create a new game board
    test_board = create_board()
    num_bombs = calculate_bomb_count(test_board, 0.15)  # 15% of tiles are bombs
    test_board = random_bomb_location(test_board, num_bombs)
    test_board = all_surrounding_mines(test_board)

    # Clear the game area and render the new board
    for widget in game_frame.winfo_children():
        widget.destroy()

    render_game_board(test_board)



def check_win_condition():
    """
    Checks if all non-bomb tiles have been revealed.
    If true, it ends the game with a "You Win!" message.
    """
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


def display_win_message():
    """
    Displays a "You Win!" message and disables all buttons.
    """
    win_label = tkinter.Label(root, text="YOU WIN!", font=("Arial", 24), fg="green", bg="white")
    win_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the message
    root.after(2000, win_label.destroy)  # Remove the message after 2 seconds

    for btn in buttons:
        btn.config(state="disabled")  # Disable all buttons to prevent further clicks




# GUI setup
root = tkinter.Tk()
root.geometry("600x600")

# Zone de jeu
game_frame = tkinter.Frame(root, bg="white")
game_frame.place(relx=0.5, rely=0.6, anchor="center")

# Bouton pour démarrer une nouvelle partie
start_button = tkinter.Button(root, text="Start Game", command=start_game)
start_button.pack(pady=10)

# Champs pour la taille du plateau
size_x = tkinter.Entry(root, width=5)
size_x.insert(0, "10")  # Valeur par défaut
size_x.pack()
size_y = tkinter.Entry(root, width=5)
size_y.insert(0, "10")  # Valeur par défaut
size_y.pack()

# Démarrage initial
# New variables for tracking win condition


start_game()
root.mainloop()
