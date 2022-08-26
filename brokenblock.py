from tkinter import *
import random


blocks = []
block_size = {"h": 75, "v": 35} # horizontal, vertical
ball = {"speed_x" : 20, #ballspeed
        "speed_y" : -20, 
        "x" : 350, #ball-position
        "y" : 300, 
        "w" : 10, #ball-diameter
        }
paddle = {"x": 0, "h": 100}
is_gameover = False
point = 0

tk = Tk()
canvas = Canvas(tk, width = 605, height= 600, bg="gray")
canvas.pack()


def __init__():
    global is_gameover, point
    is_gameover = False
    ball["y"] = 250
    ball["speed_y"] = -10
    point = 0

    # puts blocks
    for col in range(0, 5):
        for row in range(0, 8):
            color = "maroon"
            if (col + row) % 2 == 1:
                color = "RoyalBlue1"
            x1 = 3 + row * block_size["h"]
            x2 = x1 + block_size["h"]
            y1 = 5 + col * block_size["v"]
            y2 = y1 + block_size["v"]
            blocks.append([x1, y1, x2, y2, color])
    tk.title("START")
    

def draw_objects():
    canvas.delete('all')
    canvas.create_rectangle(0, 0, 605, 600, fill="gray10", width=0)

    # draw one by one block
    for b in blocks:
        x1, y1, x2, y2, color = b
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)
    
    # draw ball
    canvas.create_oval(
        ball["x"] - ball["w"], ball["y"] - ball["w"],
        ball["x"] + ball["w"], ball["y"] + ball["w"], fill="yellow")

    # draw paddle
    canvas.create_rectangle(paddle["x"], 490, paddle["x"] + paddle["h"], 500, fill="light grey")

    
def move_ball():
    global is_gameover, point
    if is_gameover:
        return
    
    
    # records value after moving 
    bx = ball["x"] + ball["speed_x"]
    by = ball["y"] + ball["speed_y"]

    # hits upper,left,right walls
    if bx < 0 or bx > 600:
        ball["speed_x"] *= -1
    if by < 0 or by > 600:
        ball["speed_y"] *= -1

    # hits paddle
    if by > 480 and (paddle["x"] <= bx <= (paddle["x"] + paddle["h"])):
        ball["speed_y"] *= -1
        if random.randint(0, 1) == 0:
            ball["speed_x"] *= -1
        by = 470

    # ball hits block
    hit_i = -1
    for i, w in enumerate(blocks):
        x1, y1, x2, y2, color = w
        w3 = ball["w"] / 3
        if (x1-w3 <= bx <= x2+w3) and (y1-w3 <= by <= y2+w3):
            hit_i = i
            break
    if hit_i >= 0:
        del blocks[hit_i]
        if random.randint(0, 1) == 0:
            ball["speed_x"] *= -1
            ball["speed_y"] *= -1
        point += 10
        tk.title("GAME SCORE = " + str(point))

    # game over
    if by >= 600:
        tk.title("GAME OVER! SCORE=" + str(point))
        is_gameover = True
    if 0 <= bx <= 600:
        ball["x"] = bx
    if 0 <= by <= 600:
        ball["y"] = by
  

def game_loop():
    draw_objects()
    move_ball()
    tk.after(50, game_loop)


def control(e):
    paddle["x"] = e.x
def click(e):
    if is_gameover:
        __init__()

tk.bind('<Motion>', control)
tk.bind('<Button-1>', click)


__init__()
game_loop()
tk.mainloop()
