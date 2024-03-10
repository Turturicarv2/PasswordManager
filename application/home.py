import tkinter as tk
import ttkbootstrap as ttk

class Home(ttk.Window):
    def __init__(self):
        # setup
        super().__init__()
        self.title('Home')
        self.geometry('800x600')
        self.minsize(width=800, height=400)

        # layout
        self.columnconfigure((0,1,2,3,4), weight = 1, uniform = 'a')
        self.rowconfigure(0, weight = 1)

        self.mainloop()

if __name__ == '__main__':
    Home()