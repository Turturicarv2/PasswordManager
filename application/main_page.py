import tkinter as tk
import ttkbootstrap as ttk
from settings import *
from PIL import Image
from login_page import login_page

class App(ttk.Window):
    def __init__(self):

        # setup
        super().__init__(themename='lumen')
        self.title('Welcome!')
        self.geometry('800x600')
        self.minsize(width=800, height=400)

        # layout
        self.columnconfigure((0,1,2,3,4), weight = 1, uniform = 'a')
        self.rowconfigure(0, weight = 1)

        # create image
        self.image = Image.open('images/main_image.jpg')
        self.image_ratio = self.image.size[0] / self.image.size[1]

        # create widgets
        self.create_widgets()

        # bindings
        self.canvas.bind('<Configure>', lambda event: fill_image(self.image, self.image_ratio, self.canvas, event))

        # mainloop
        self.mainloop()
    
    def create_widgets(self):
        app_description = ("Welcome to my application! This is a platform where you can store your passwords "
                   "for all kinds of services. If you want to be secure on the internet, this application has got you covered!")
        
        login_frame = ttk.Frame(self)
        ttk.Label(login_frame, text='Welcome! Would you like to sign in?', font=(FONT, TEXT_SIZE), bootstyle = 'SECONDARY').pack()
        login_button = ttk.Button(login_frame, text='Sign in', command=self.open_login_page).pack(pady = 10)
        ttk.Button(login_frame, text='Sign up').pack(pady = 10)
        ttk.Label(login_frame, text=app_description, font=(FONT, TEXT_SIZE), bootstyle = 'INFO', wraplength=250, justify="center").pack(pady = 70)

        self.canvas = tk.Canvas(self, bd = 0, highlightthickness=0, relief = 'ridge')
        self.canvas.grid(column=0, row=0, columnspan=3, sticky='nsew')

        login_frame.grid(column = 3, row = 0, columnspan=2, sticky='ew', padx = 40)

    def open_login_page(self):
        self.withdraw()
        login_page(self)

if __name__ == '__main__':
    App()
    