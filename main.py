from tkinter import *
from play_window import Snake
from loading import Loading


class App(Tk):
    __settings_but = {
        'bg': 'black',
        'fg': 'white',
        'h': 3,
        'w': 25
    }

    def __init__(self):
        Tk.__init__(self)
        self.attributes('-alpha', 1)
        self.attributes('-topmost', True)
        self.resizable(False, False)
        self.geometry("400x400+500+200")
        self.title("Змейка")
        self["bg"] = "white"
        self.set_menu()

    def set_menu(self):
        self.but_play = Button(text="Начать новую игру",
                               command=self.run,
                               background=App.__settings_but["bg"],
                               foreground=App.__settings_but["fg"],
                               height=App.__settings_but["h"],
                               width=App.__settings_but["w"],
                               bd=0)
        self.but_play.pack(expand=1)
        self.but_play.bind('<Enter>', Snake.enter_leave)
        self.but_play.bind('<Leave>', Snake.enter_leave)
        self.but_load = Button(text="Загрузить игру",
                               command=self.load,
                               background=App.__settings_but["bg"],
                               foreground=App.__settings_but["fg"],
                               height=App.__settings_but["h"],
                               width=App.__settings_but["w"],
                               bd=0)
        self.but_load.pack(expand=1)
        self.but_load.bind('<Enter>', Snake.enter_leave)
        self.but_load.bind('<Leave>', Snake.enter_leave)
        self.but_exit = Button(text="Выйти",
                               command=self.exit,
                               background=App.__settings_but["bg"],
                               foreground=App.__settings_but["fg"],
                               height=App.__settings_but["h"],
                               width=App.__settings_but["w"],
                               bd=0)
        self.but_exit.pack(expand=1)
        self.but_exit.bind('<Enter>', Snake.enter_leave)
        self.but_exit.bind('<Leave>', Snake.enter_leave)

    def run(self):

        Snake(self)

    def del_menu(self):
        self.but_play.pack_forget()
        self.but_load.pack_forget()
        self.but_exit.pack_forget()

    def exit(self):
        self.destroy()

    def load(self):
        Loading(self)





app = App()

app.mainloop()
