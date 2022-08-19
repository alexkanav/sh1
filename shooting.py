import tkinter as tk
from  random import randint, choice
import math
import time

WIDTH=800
HIGHT=600
balls = {}

class Game_menu(tk.Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Тир")

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar)
        file_menu.add_command(label="Новая игра", command=self.finish)
        file_menu.add_command(label="Выйти", command=self.on_exit)
        menubar.add_cascade(label="Игра", menu=file_menu)

    def finish(self):
        if 'frame' in globals():
            new_game('on')
        else:
            end_game('menu')

    def on_exit(self):
        quit()


class Ball:
    def __init__(self, dx, dy):
        self.color = choice(['blue', 'green', 'red', 'brown', 'yellow'])
        self.x = 50
        self.y = 420
        self.r = 10
        self.dx = dx
        self.dy = dy
        self.ball_id = canvas.create_oval(self.x - self.r, self.y - self.r,
                                          self.x + self.r, self.y + self.r,
                                          fill=self.color )
        self.live_ball = time.time()

    def move(self):
        if self.x + self.dx >= WIDTH or self.x + self.dx <= 0:
            self.dx = -self.dx
        else:
            self.x += self.dx
        if self.y - self.dy >= HIGHT or self.y - self.dy <= 0:
            self.dy = -self.dy
        else:
            self.y -= self.dy
        self.dy -= 0.5

    def show(self):
        canvas.coords(self.ball_id, self.x - self.r, self.y - self.r,
                                          self.x + self.r, self.y + self.r)
        self.dx -= 0.05 * self.dx / abs(self.dx)
        self.dy -= 0.05 * self.dy / abs(self.dy)

    def hitting(self):
        if (self.x + self.r) >= 790 and g_new_target.y <= self.y <= (g_new_target.y + g_new_target.lenght):
            end_game('hitt')


class Gun:
    def __init__(self):
        self.x_gun = 50
        self.y_gun = 420
        self.power_growing = 10
        self.power_on = 0
        self.id = canvas.create_line(20, 450, 50, 420, width=7)
        self.corner = 1

    def gun_power(self):
        if self.power_on:
            if self.power_growing < 100:
                self.power_growing += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
            self.power_growing = 10

    def gun_aiming(self, event):
        if event:
            self.corner = math.atan((event.y - 429) / (event.x - -1)) # 450 and 20 for (event.x - 20) maybe division by zero

    def show(self):
        canvas.coords(self.id, 20, 450,
                        20 + max(self.power_growing, 20) * math.cos(self.corner),
                        450 + max(self.power_growing, 20) * math.sin(self.corner)
                        )


class Target:
    def __init__(self):
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.lenght = 30
        self.x = 792
        self.y = randint(50, HIGHT - 50)
        self.target_id = canvas.create_line(self.x, self.y, self.x, self.y + self.lenght, fill=self.color, width=7)
    def show(self):
        canvas.coords(self.x, self.y, self.x, self.y + self.lenght)


def start_new_game():
    global number_target, shot_number, game_on, g_new_gun, g_new_target, balls
    balls = {}
    number_target = 0
    shot_number = 0
    canvas.itemconfig(label_score, text='')
    add_gun()
    add_target()
    game_on = 1

def add_gun():
    global g_new_gun
    g_new_gun = Gun()


def add_target():
    global g_new_target, number_target
    g_new_target = Target()
    number_target += 1


def gun_growing_start(event):
    g_new_gun.power_growing = 10
    g_new_gun.power_on = 1

def gun_growing_stop_shot(event):
    global shot_number
    shot_number += 1
    add_ball()
    g_new_gun.power_on = 0

def add_ball():
    dx = g_new_gun.power_growing / 5
    dy = dx * abs(math.tan(g_new_gun.corner))
    balls['ball_%d' % shot_number] = Ball(dx, dy)

def tick():
    if game_on == 1:
        g_new_gun.show()
        g_new_target.show()
        g_new_gun.gun_power()
        canvas.bind('<Button-3>', gun_growing_start)
        canvas.bind('<ButtonRelease-3>', gun_growing_stop_shot)
        canvas.bind('<Motion>', g_new_gun.gun_aiming)
        if 'balls' in globals():
            for key in balls:
                balls[key].move()
                balls[key].show()
                balls[key].hitting()
                if time.time() - balls[key].live_ball > 10:
                    canvas.delete(balls[key].ball_id)
                    del balls[key]
                    break
    root.after(10, tick)

def end_game(source):
    global balls, frame, shot_number, game_on, g_new_gun, g_new_target, score
    canvas.delete(g_new_gun.id)
    canvas.delete(g_new_target.target_id)
    canvas.itemconfig(label_score, text=' Ваш счет = ' + str(score) + '\nЧисло попыток = ' + str(shot_number))
    for i in range(len(balls)):
        canvas.delete(balls['ball_%d' % shot_number].ball_id)
        shot_number -= 1
    # [balls.pop(key, None) for key in["ball_1", "'ball_%d' % shot_number"]]
    game_on = 0
    del g_new_gun
    del g_new_target
    if source == 'hitt':
        score += 1
        frame = tk.Frame(master=root, width=800, height=40)
        frame.pack()
        button1 = tk.Button(master=frame, text="Выити", bg="red")
        button1.bind('<Button-1>', quit)
        button1.place(x=300, y=5)
        button2 = tk.Button(master=frame, text="Новая игра", bg="green")
        button2.bind('<Button-1>', new_game)
        button2.place(x=400, y=5)
    else:
        start_new_game()
def new_game(event):
    global frame
    frame.destroy()
    del frame
    start_new_game()


def main():
    global root, score, WIDTH, HIGHT, canvas, g_new_game, label_score
    root=tk.Tk()
    root.geometry(str(WIDTH)+ 'x' + str(HIGHT))
    canvas = tk.Canvas(root, bg='yellow')
    canvas.pack(expand=1, fill='both') # or fill=tk.BOTH
    add_menu = Game_menu()
    score = 1
    label_score = canvas.create_text(100, 50, text='')
    start_new_game()
    tick()
    root.mainloop()

main()
