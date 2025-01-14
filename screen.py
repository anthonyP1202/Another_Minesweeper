import tkinter

def put_flaged():
    pass

def reveal_mine():
    pass



root = tkinter.Tk()
root.geometry("1728x864")

size_width = 1728
size_heigh = 864

canvas = tkinter.Canvas(root, width=size_width, height=size_heigh, bg="white")
canvas.pack()

settings_background = canvas.create_rectangle(size_width*0.1,size_heigh*0.1 ,size_width*0.9,size_heigh*0.15, fill="#8F908F", outline="#CCCCCC") #header
game_background = canvas.create_rectangle(size_width*0.1,size_heigh*0.15,size_width*0.9,size_heigh*0.9, fill="#B6B6B6", outline="#CCCCCC") #play area

button_width = 100
button_height = 20

# Calculate button position (centered in the play area)
x_center = (size_width * 0.1 + size_width * 0.9) / 2 - button_width / 2
y_center = (size_heigh * 0.1 + size_heigh * 0.15) / 2 - button_height / 2

# Create and place the button
start_button = tkinter.Button(root, text="o", background="#8D8D8D")
start_button.place(x=x_center, y=y_center)

root.mainloop() # start 