import tkinter as tk
import ttkbootstrap as ttk

class Home(ttk.Window):
    def __init__(self, main_window, user_id):
        # setup
        super().__init__()
        self.title('Home')
        self.geometry('800x600')
        self.minsize(width=800, height=400)

        self.mainloop()


class PasswordArea(ttk.Frame):
    def __init__(self):
        super().__init__()

    def list_passwords(self):
        ttk.Label(text = 'Website').pack(side = 'left')
        ttk.Label(text = 'Username').pack(side = 'left')
        ttk.Label(text = 'Password').pack(side = 'left')
        for i in range(5):
            ttk.Label(text = '')


if __name__ == '__main__':
    Home()