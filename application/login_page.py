import tkinter as tk
import ttkbootstrap as ttk
from settings import *
from PIL import Image



class login_page(ttk.Toplevel):
    def __init__(self, main_window):

        # setup
        self.main_window = main_window
        super().__init__()
        self.title('Sign in')
        self.geometry('800x600')
        self.minsize(width=800, height=400)

        # layout
        self.columnconfigure((0,1,2,3,4), weight = 1, uniform = 'a')
        self.rowconfigure(0, weight = 1)

        # create image
        self.image = Image.open('images/login_image.jpg')
        self.image_ratio = self.image.size[0] / self.image.size[1]

        # create widgets
        self.create_widgets()

        # bindings
        self.canvas.bind('<Configure>', lambda event: stretch_image(self.image, self.image_ratio, self.canvas, event))

        # mainloop
        self.mainloop()
    
    def create_widgets(self):
        login_frame = ttk.Frame(self)
        ttk.Label(login_frame, text='Username:', font=(FONT, TEXT_SIZE), bootstyle = 'SECONDARY').pack()
        ttk.Entry(login_frame, bootstyle = 'PRIMARY').pack(pady = 5)
        ttk.Label(login_frame, text='Password:', font=(FONT, TEXT_SIZE), bootstyle = 'SECONDARY').pack()
        ttk.Entry(login_frame, show='*', bootstyle = 'PRIMARY').pack(pady = 5)
        ttk.Button(login_frame, text='Log in').pack(pady = 20)
        home = ttk.Label(self, text = '< Back', bootstyle = 'SECONDARY')
        home.bind('<Button>', self.open_home_page)
        home.place(x = 20, y = 20, anchor='nw')

        self.canvas = tk.Canvas(self, bd = 0, highlightthickness=0, relief = 'ridge', background='black')
        self.canvas.grid(column=2, row=0, columnspan=3, sticky='nsew')

        login_frame.grid(column = 0, row = 0, columnspan=2, sticky='ew', padx = 40)

    def open_home_page(self, event):
        self.destroy()
        self.update()
        self.main_window.deiconify()
        