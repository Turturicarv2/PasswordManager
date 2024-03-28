import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
from settings import *
from PIL import Image
import requests
from login_page import login_page



class signup_page(ttk.Toplevel):
    def __init__(self, main_window):

        # setup
        self.main_window = main_window
        super().__init__()
        self.title('Sign up')
        self.geometry('800x600')
        self.minsize(width=800, height=400)

        # layout
        self.columnconfigure((0,1,2,3,4), weight = 1, uniform = 'a')
        self.rowconfigure(0, weight = 1)

        # create image
        self.image = Image.open('images/signup_image.jpg')
        self.image_ratio = self.image.size[0] / self.image.size[1]

        # create widgets
        self.create_widgets()

        # bindings
        self.canvas.bind('<Configure>', lambda event: stretch_image(self.image, self.image_ratio, self.canvas, event))
        self.protocol("WM_DELETE_WINDOW", self.close_app)

        # mainloop
        self.mainloop()
    
    def create_widgets(self):
        login_frame = ttk.Frame(self)
        ttk.Label(login_frame, text='Email:', font=(FONT, TEXT_SIZE), bootstyle = 'SECONDARY').pack()
        self.mail_entry = ttk.Entry(login_frame, bootstyle = 'PRIMARY')
        self.mail_entry.pack(pady = 5)
        ttk.Label(login_frame, text='Username:', font=(FONT, TEXT_SIZE), bootstyle = 'SECONDARY').pack()
        self.username_entry = ttk.Entry(login_frame, bootstyle = 'PRIMARY')
        self.username_entry.pack(pady = 5)
        ttk.Label(login_frame, text='Password:', font=(FONT, TEXT_SIZE), bootstyle = 'SECONDARY').pack()
        self.password_entry = ttk.Entry(login_frame, show='*', bootstyle = 'PRIMARY')
        self.password_entry.pack(pady = 5)
        ttk.Label(login_frame, text='Repeat Password:', font=(FONT, TEXT_SIZE), bootstyle = 'SECONDARY').pack()
        self.password_reentry = ttk.Entry(login_frame, show='*', bootstyle = 'PRIMARY')
        self.password_reentry.pack(pady = 5)
        ttk.Button(login_frame, text='Sign up', command=self.signup_button_command).pack(pady = 20)
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
      
    def close_app(self):
        self.main_window.destroy()

    def signup_button_command(self):
        password = self.password_entry.get()
        password_check = self.password_reentry.get()

        username = self.username_entry.get()
        email = self.mail_entry.get()

        if password != password_check:
            Messagebox.show_error('Your passwords are not the same!', title = 'Error', parent = self, alert=True)
        # TODO: Add email + user check here! 
        elif len(username) < 6:
            Messagebox.show_error('Your username is too short!', title = 'Error', parent = self, alert=True)
        elif len(password) < 8:
            Messagebox.show_error('Your password is too short!', title = 'Error', parent = self, alert=True)
        else:
            url = "https://turturicar.pythonanywhere.com/create_user/"

            # Adding a payload
            payload = {"username": username, "email": email, "password": password}

            # A get request to the server
            connection = requests.post(url, json = payload)

            response = connection.json()

            if response['success'] == True:
                # TODO: Add some sort of success message
                self.destroy()
                self.update()
                login_page(main_window=self.main_window)
            else:
                Messagebox.show_error('Oops, something went wrong', title = 'Error', parent = self, alert=True)