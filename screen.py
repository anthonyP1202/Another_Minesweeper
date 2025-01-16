import tkinter
from tile import tile
import random

def put_flaged(tile):
    pass

def reveal_mine(tile):
    pass

def create_board():
    x = 10
    y = 10
    
    try :
        x = int(size_x.get())
        y = int(size_y.get())
    except:
        pass
    
    board=[]
    for cs in range(x):
        row=[]
        for i in range(y):
            frame = tile(location=[x, y])
            row.append(frame)
        board.append(row)
    return board  # Return the 2D list of tiles



def random_bomb_location(table,numb_bomb):
    trash=[]
    rows = len(table)
    cols = len(table[0]) if rows > 0 else 0
    rand_row=0
    rand_col=0

    for rando in range(numb_bomb):
        rand_row=random.randint(0,rows-1)
        rand_col=random.randint(0,cols-1)
        if [rand_row,rand_col] in trash:
            rando-=1
        else:
            trash.append([rand_row,rand_col])
            table[rand_row][rand_col].is_mine=True
    
    return table




root = tkinter.Tk()
root.geometry("1728x864")

size_width = 1728
size_heigh = 864

# background
canvas = tkinter.Canvas(root, width=size_width, height=size_heigh, bg="white") 
canvas.pack()

settings_background = canvas.create_rectangle(size_width*0.1,size_heigh*0.1 ,size_width*0.9,size_heigh*0.15, fill="#8F908F", outline="#CCCCCC") #header
game_background = canvas.create_rectangle(size_width*0.1,size_heigh*0.15,size_width*0.9,size_heigh*0.9, fill="#B6B6B6", outline="#CCCCCC") #play area

button_width = 100
button_height = 20



# Calculate button position (centered in the play area)
x_center = (size_width * 0.1 + size_width * 0.9) / 2 - 100 / 2
y_center = (size_heigh * 0.1 + size_heigh * 0.15) / 2 - 20 / 2

# Create and place the button
start_button = tkinter.Button(root, text="o", background="#8D8D8D", command=create_board)
start_button.place(x=x_center, y=y_center)

# board size settings
size_x = tkinter.Entry(root, width=5)
size_x.place(x=x_center - 100, y=y_center)
size_y = tkinter.Entry(root, width=5)
size_y.place(x=x_center + 95, y=y_center)

# root.mainloop() # start 

test_board=create_board()
test_board2=random_bomb_location(test_board,10)
is_mine_matrix = [[tile.is_mine for tile in row] for row in test_board2]

# Print the matrix
for row in is_mine_matrix:
    print(row)
