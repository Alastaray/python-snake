from tkinter import *
from tkinter import messagebox
from play_window import Snake
from os.path import exists


class Loading:
    def __init__(self, app):
        self.file_path = "saves.txt"
        self.between = 0
        self.widget_save = []
        self.widget_save_ind = 0
        self.x = []
        self.y = []
        self.score = []
        self.time = []
        self.move_direction = []
        self.body_size = []
        self.page_saves = 0
        self.limit_saves = 2
        self.app = app
        self.but_back = (Button(text="Назад", command=self.go_to_menu,
                                background=Snake.settings_but["bg"],
                                foreground=Snake.settings_but["fg"],
                                bd=0, font='Times 10'))
        self.but_left = (Button(text="<<", command=self.pagination_de,
                                background=Snake.settings_but["bg"],
                                foreground=Snake.settings_but["fg"],
                                bd=0, font='Times 10'))
        self.but_right = (Button(text=">>", command=self.pagination_in,
                                 background=Snake.settings_but["bg"],
                                 foreground=Snake.settings_but["fg"],
                                 bd=0, font='Times 10'))
        self.app_load()

    def app_load(self):

        if exists(self.file_path):
            self.widget_save = []
            self.widget_save_ind = 0
            self.x = []
            self.y = []
            self.score = []
            self.time = []
            self.move_direction = []
            self.body_size = []
            self.between = 0
            self.app.del_menu()
            file = open(self.file_path, "+r")
            self.save_collection(file)
            file.close()
            self.placed_saves()
        else:
            messagebox.showinfo("Ошибка", "Сохранений не существует!")

    def save_collection(self, file):
        while True:
            line = file.readline()
            if not line:
                break
            if line[0] == 'x':
                x = line.split('-')
                for i in range(1, len(x)):
                    x[i] = int(x[i])
                x.pop(0)
                self.x.append(x)
            if line[0] == 'y':
                y = line.split('-')
                for i in range(1, len(y)):
                    y[i] = int(y[i])
                y.pop(0)
                self.y.append(y)
            if line[0] == 's':
                score = line.split('-')
                self.score.append(int(score[1]))
            if line[0] == 'b':
                body = line.split('-')
                self.body_size.append(int(body[1]))
            if line[0] == 'm':
                move = line.split('-')
                self.move_direction.append(move[1])
            if line[0] == 't':
                time = line.split('/')
                self.time.append(time[1])
            if line[0] == '*':
                self.create_but_save()

    def create_but_save(self):
        self.widget_save.append(Button(text="\nСчёт " + str(self.score[self.widget_save_ind]) +
                                            "\t\t\t\t" + str(self.time[self.widget_save_ind]),
                                       background=Snake.settings_but["bg"],
                                       foreground=Snake.settings_but["fg"],
                                       height=3, width=60, bd=0,
                                       font='Times 10'))
        self.widget_save_ind += 1

    def placed_saves(self):

        for i in range((self.limit_saves * self.page_saves), (self.limit_saves * self.page_saves) + self.limit_saves):
            if i >= self.widget_save_ind:
                break
            self.widget_save[i].place(x=0, y=self.between)
            self.widget_save[i].bind \
                ("<Button-1>", lambda event, ind=i: self.loading(event, ind))
            self.widget_save[i].bind \
                ("<Button-3>", lambda event, ind=i: self.del_saves(event, ind))
            self.widget_save[i].bind('<Enter>', Snake.enter_leave)
            self.widget_save[i].bind('<Leave>', Snake.enter_leave)
            if i <= (self.limit_saves * self.page_saves) + self.limit_saves:
                self.between += 60

        self.but_back.place(x=180, y=370)
        self.but_back.bind('<Enter>', Snake.enter_leave)
        self.but_back.bind('<Leave>', Snake.enter_leave)
        self.but_left.place(x=150, y=370)
        self.but_left.bind('<Enter>', Snake.enter_leave)
        self.but_left.bind('<Leave>', Snake.enter_leave)
        self.but_right.place(x=230, y=370)
        self.but_right.bind('<Enter>', Snake.enter_leave)
        self.but_right.bind('<Leave>', Snake.enter_leave)

    def loading(self, event, ind):
        self.go_to_menu()
        if self.move_direction[ind] == 'd\n':
            Snake(self.app, x=self.x[ind], y=self.y[ind], move_right=False, move_down=True,
                  body_size=self.body_size[ind], score=self.score[ind])
        if self.move_direction[ind] == 'u\n':
            Snake(self.app, x=self.x[ind], y=self.y[ind], move_right=False, move_up=True,
                  body_size=self.body_size[ind], score=self.score[ind])
        if self.move_direction[ind] == 'l\n':
            Snake(self.app, x=self.x[ind], y=self.y[ind], move_right=False, move_left=True,
                  body_size=self.body_size[ind], score=self.score[ind])
        if self.move_direction[ind] == 'r\n':
            Snake(self.app, x=self.x[ind], y=self.y[ind],
                  body_size=self.body_size[ind], score=self.score[ind])

    def pagination_in(self):
        for i in range((self.limit_saves * self.page_saves), (self.limit_saves * self.page_saves) + self.limit_saves):
            if i >= self.widget_save_ind:
                break
            self.widget_save[i].place_forget()
        if self.page_saves < self.widget_save_ind / self.limit_saves-1:
            self.page_saves += 1
        self.between = 0
        self.placed_saves()

    def pagination_de(self):
        for i in range((self.limit_saves * self.page_saves), (self.limit_saves * self.page_saves) + self.limit_saves):
            if i >= self.widget_save_ind:
                break
            self.widget_save[i].place_forget()
        if self.page_saves > 0:
            self.page_saves -= 1
        self.between = 0
        self.placed_saves()

    def go_to_menu(self):
        self.but_back.place_forget()
        self.but_left.place_forget()
        self.but_right.place_forget()
        self.del_but_save()
        self.app.set_menu()

    def del_but_save(self):
        for i in range(0, self.widget_save_ind):
            self.widget_save[i].place_forget()

    def del_saves(self, event, ind):
        self.widget_save[ind].place_forget()
        file = open(self.file_path, "+r")
        lines = file.readlines()
        file.close()
        i = 0
        counter_stars = 0
        while True:
            if i >= len(lines):
                break
            if lines[i][0] == '*':
                if counter_stars == ind:
                    for j in range(i, i - 7, -1):
                        lines[j] = ''
                counter_stars += 1
            i += 1

        file = open(self.file_path, "+w")
        file.writelines(lines)
        file.close()
        self.del_but_save()
        self.app_load()
