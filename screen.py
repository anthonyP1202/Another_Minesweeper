import tkinter
from tile import tile

def put_flaged(tile, button = tkinter.Button):
    if tile.is_flagged == True:
        tile.is_flagged = False
        button.config(text="")
    else:
        tile.is_flagged = True
        button.config(text="P")
    
    print(type(tile))
    print(type(button))

def reveal_mine(tile, button):
    print(tile.is_mine)

def create_board():
    x = 20 
    y = 20
    
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

    for f in range(x):
        for g in range(y):
            bton = tkinter.Button(root, width=5, height=5)
            # Bind left-click to reveal_mine and right-click to put_flaged
            bton.bind("<Button-1>", lambda event, f=f, g=g, bton=bton: reveal_mine(board[f][g], bton))
            bton.bind("<Button-3>", lambda event, f=f, g=g, bton=bton: put_flaged(board[f][g], bton))
            bton.place(x=g * 20 + x_center/2, y=f * 20 + y_center * 1.9)
            #  bton.place(x=x_center/2 + g * 30, y=y_center + f * 30)

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

root.mainloop() # start 