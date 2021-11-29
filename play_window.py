from tkinter import *
from tkinter import messagebox
from urllib.request import urlopen

from PIL import Image, ImageTk
import random
from os.path import exists
from datetime import datetime
import inspect


class Snake:
    __color = ["black", "green", "yellow", "blue", "purple", "orange"]
    settings_but = {
        'bg': 'black',
        'fg': 'white',
        'h': 3,
        'w': 25
    }

    def __init__(self, parent, x=0, y=0, body_size=5,score=0,
                 move_right=True, move_left=False, move_down=False,  move_up=False):

        self.parent = parent
        self.parent.withdraw()
        self.root = Toplevel(self.parent)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.score_label = 0
        self.score = score
        self.title_score = Label(self.root, text="Счёт ", bg="white", font='Times 20')
        self.title_score.place(x=20, y=20)
        self.menu_but = Button(self.root, text="Меню", bd=0, fg="white", bg="black",
                               font='Times 10', command=self.menu)
        self.menu_but.place(x=360, y=0)
        self.menu_but.bind('<Enter>', Snake.enter_leave)
        self.menu_but.bind('<Leave>', Snake.enter_leave)
        self.__set_root()
        self.__set_coords()
        self.__set_body(body_size, x, y, move_right, move_left, move_down,  move_up)
        self.create_snake()
        self.create_apple()

    def __set_root(self):
        self.root.attributes('-alpha', 1)
        self.root.attributes('-topmost', True)
        self.root.resizable(False, False)
        self.root.geometry("400x400")
        self.root.title("Змейка")
        self.root["bg"] = "white"
        self.root.bind_all('<Key>', self.move)

    def __set_coords(self):
        self.x = []
        self.y = []
        self.ax = 0
        self.ay = 0
        self.speed = 14

    def __set_body(self, body_size, x, y,
                   move_right, move_left, move_down,  move_up):
        self.body = list()
        self.body_size = body_size
        self.limb_size = 10
        self.range_limb = self.limb_size + 4
        self.apple = Label(self.root, image=ImageTk.PhotoImage(Image.open("dot.png")),
                           bg="red", height=self.limb_size, width=self.limb_size)
        self.cancel_apple = 0
        self.cancel_snake = 0
        self.move_right = move_right
        self.move_left = move_left
        self.move_down = move_down
        self.move_up = move_up
        for i in range(0, self.body_size):
            self.body.append(Label(self.root, image=ImageTk.PhotoImage(Image.open("dot.png")),
                                   bg=Snake.__color[random.randint(0, len(Snake.__color) - 1)],
                                   height=self.limb_size, width=self.limb_size))
            if isinstance(x, list) and isinstance(y, list):
                self.x.append(x[i])
                self.y.append(y[i])
            else:
                self.x.append(i * self.limb_size + 4)
                self.y.append(0)

        self.placed_body()

    def menu(self):
        self.root.after_cancel(self.cancel_apple)
        self.root.after_cancel(self.cancel_snake)
        self.but_continue = Button(self.root, text="Продолжить",
                                   command=self.del_menu,
                                   background=Snake.settings_but["bg"],
                                   foreground=Snake.settings_but["fg"],
                                   height=Snake.settings_but["h"],
                                   width=Snake.settings_but["w"],
                                   bd=0)
        self.but_continue.pack(expand=1)
        self.but_continue.bind('<Enter>', Snake.enter_leave)
        self.but_continue.bind('<Leave>', Snake.enter_leave)
        self.but_replay = Button(self.root, text="Начать игру заново",
                                 command=self.replay,
                                 background=Snake.settings_but["bg"],
                                 foreground=Snake.settings_but["fg"],
                                 height=Snake.settings_but["h"],
                                 width=Snake.settings_but["w"],
                                 bd=0)
        self.but_replay.pack(expand=1)
        self.but_replay.bind('<Enter>', Snake.enter_leave)
        self.but_replay.bind('<Leave>', Snake.enter_leave)

        self.but_save = Button(self.root, text="Сохранить игру",
                               command=self.save,
                               background=Snake.settings_but["bg"],
                               foreground=Snake.settings_but["fg"],
                               height=Snake.settings_but["h"],
                               width=Snake.settings_but["w"],
                               bd=0)
        self.but_save.pack(expand=1)
        self.but_save.bind('<Enter>', Snake.enter_leave)
        self.but_save.bind('<Leave>', Snake.enter_leave)

        self.but_exit = Button(self.root, text="Выйти",
                               command=self.close,
                               background=Snake.settings_but["bg"],
                               foreground=Snake.settings_but["fg"],
                               height=Snake.settings_but["h"],
                               width=Snake.settings_but["w"],
                               bd=0)
        self.but_exit.pack(expand=1)
        self.but_exit.bind('<Enter>', Snake.enter_leave)
        self.but_exit.bind('<Leave>', Snake.enter_leave)

    def replay(self):
        self.close(False)
        Snake(self.parent)

    def save(self):
        file_path = "saves.txt"
        if exists(file_path):
            file = open(file_path, "+a")
            self.write_saves(file)
        else:
            file = open(file_path, "+w")
            self.write_saves(file)
        file.close()
        self.del_menu()

    def write_saves(self, file):
        file.write("x")
        for el in self.x:
            file.write("-" + str(el))
        file.write("\n")
        file.write("y")
        for el in self.y:
            file.write("-" + str(el))
        file.write("\n")
        file.write("s" + "-" + str(self.score) + "\n")
        file.write("b" + "-" + str(self.body_size) + "\n")
        file.write("t" + "/" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        if self.move_down:
            file.write("m-d" + "\n")
        if self.move_up:
            file.write("m-u" + "\n")
        if self.move_left:
            file.write("m-l" + "\n")
        if self.move_right:
            file.write("m-r" + "\n")
        file.write("*" + "\n")

    def del_menu(self):
        self.cancel_apple = self.root.after(10000, self.create_apple)
        self.cancel_snake = self.root.after(100, self.create_snake)
        self.but_continue.pack_forget()
        self.but_replay.pack_forget()
        self.but_save.pack_forget()
        self.but_exit.pack_forget()

    def close(self, arg=True):
        if arg:
            self.root.after_cancel(self.cancel_apple)
            self.root.after_cancel(self.cancel_snake)
            self.parent.deiconify()
            self.root.destroy()
            messagebox.showinfo("Конец", "Игра окончена со счётом " + str(self.score))
        else:
            self.root.destroy()

    def increase_body(self):
        self.body.append(Label(self.root, image=ImageTk.PhotoImage(Image.open("dot.png")),
                               bg=Snake.__color[random.randint(0, len(Snake.__color) - 1)],
                               height=self.limb_size, width=self.limb_size))
        self.body_size += 1

    def placed_body(self):

        if self.move_down:
            for i in range(self.body_size - 1, -1, -1):
                self.body[i].place(x=self.x[i], y=self.y[i])

        if self.move_up:
            for i in range(self.body_size - 1, -1, -1):
                self.body[i].place(x=self.x[i], y=self.y[i])

        if self.move_left:
            for i in range(self.body_size - 1, -1, -1):
                self.body[i].place(x=self.x[i], y=self.y[i])

        if self.move_right:
            for i in range(self.body_size - 1, -1, -1):
                self.body[i].place(x=self.x[i], y=self.y[i])

    def set_score_label(self):
        self.score_label = Label(self.root, text=str(self.score),
                                 bg="white", font='Times 20')
        self.score_label.place(x=100, y=20)

    def increase_x(self):
        last_ind = self.body_size - 1
        if self.move_left:
            self.x.append(self.x[last_ind] - self.range_limb)
        elif self.move_right:
            self.x.append(self.x[last_ind] + self.range_limb)
        else:
            self.x.append(self.x[last_ind])

    def increase_y(self):
        last_ind = self.body_size - 1
        if self.move_up:
            self.y.append(self.y[last_ind] - self.range_limb)
        elif self.move_down:
            self.y.append(self.y[last_ind] + self.range_limb)
        else:
            self.y.append(self.y[last_ind])

    def set_x_y(self, x, y):
        _x = x
        _y = y
        for i in range(self.body_size - 1, -1, -1):
            bx = self.x[i]
            by = self.y[i]

            self.x[i] = _x
            self.y[i] = _y

            _x = bx
            _y = by

    def check_x_y(self):

        last_ind = self.body_size - 1
        if self.x[last_ind] > 399:
            self.set_x_y(0, self.y[last_ind])

        if self.x[last_ind] < 0:
            self.set_x_y(399, self.y[last_ind])

        if self.y[last_ind] > 399:
            self.set_x_y(self.x[last_ind], 0)

        if self.y[last_ind] < 0:
            self.set_x_y(self.x[last_ind], 399)

        for i in range(last_ind, -1, -1):
            for j in range(last_ind, -1, -1):
                if i != j and self.x[i] == self.x[j] and self.y[i] == self.y[j]:
                    self.root.after(100, self.close)

    def check_apple(self):
        last_ind = self.body_size - 1
        if (self.y[last_ind] + self.range_limb / 2 >=
            self.ay
            >= self.y[last_ind] - self.range_limb / 2) and \
                (self.x[last_ind] + self.range_limb / 2 >=
                 self.ax
                 >= self.x[last_ind] - self.range_limb / 2):
            self.score += 1
            if self.score % 3 == 0 and self.score != 0:
                self.increase_y()
                self.increase_x()
                self.increase_body()
            self.create_apple()

    def create_snake(self):
        last_ind = self.body_size - 1

        if self.move_down:
            self.set_x_y(self.x[last_ind],
                         self.y[last_ind] + self.speed)
        if self.move_up:
            self.set_x_y(self.x[last_ind],
                         self.y[last_ind] - self.speed)
        if self.move_left:
            self.set_x_y(self.x[last_ind] - self.speed,
                         self.y[last_ind])
        if self.move_right:
            self.set_x_y(self.x[last_ind] + self.speed,
                         self.y[last_ind])
        self.check_x_y()
        self.placed_body()
        self.check_apple()
        self.cancel_snake = self.root.after(100, self.create_snake)

    def create_apple(self):
        self.set_score_label()
        if self.cancel_apple != 0:
            self.root.after_cancel(self.cancel_apple)
        self.ax = random.randint(0, 384)
        self.ay = random.randint(0, 384)
        self.apple.place(x=self.ax, y=self.ay)
        self.cancel_apple = self.root.after(10000, self.create_apple)

    def move(self, event):
        if (event.char == 'd' or event.keysym == "Right" or event.char == 'в') \
                and not self.move_left:
            self.move_right = True
            self.move_left = False
            self.move_down = False
            self.move_up = False
        if (event.char == 'a' or event.keysym == "Left" or event.char == 'ф') \
                and not self.move_right:
            self.move_right = False
            self.move_left = True
            self.move_down = False
            self.move_up = False
        if (event.char == 's' or event.keysym == "Down" or event.char == 'ы') \
                and not self.move_up:
            self.move_right = False
            self.move_left = False
            self.move_down = True
            self.move_up = False
        if (event.char == 'w' or event.keysym == "Up" or event.char == 'ц') \
                and not self.move_down:
            self.move_right = False
            self.move_left = False
            self.move_down = False
            self.move_up = True
        self.check_x_y()

    @staticmethod
    def enter_leave(event):
        if event.type == '7':
            event.widget['background'] = "white"
            event.widget['foreground'] = "black"
        elif event.type == '8':
            event.widget['background'] = "black"
            event.widget['foreground'] = "white"
