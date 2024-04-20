import tkinter as tk
import ttkbootstrap as ttk
import requests
from password_table import PasswordTable
from settings import *

class Home(ttk.Toplevel):
    def __init__(self, main_window = None, user_id = 1):
        # setup
        self.main_window = main_window
        super().__init__()
        self.user_id = user_id
        self.title('Home')
        self.geometry('850x600')
        self.minsize(width=850, height=600)

        # grid layout
        self.columnconfigure((0,1,2,3,4, 5), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1, uniform='a')

        # place widgets
        self.create_widgets()

        # bindings
        self.protocol("WM_DELETE_WINDOW", self.close_app)

        # mainloop
        self.mainloop()

    def close_app(self):
        if self.main_window:
            self.main_window.destroy()
        else:
            global app
            app.destroy()

    def create_widgets(self):
        self.create_nav_bar()
        self.create_generate_password_field()
        self.create_password_field()

    def create_nav_bar(self):
        nav_bar = ttk.Frame(master=self)
        nav_bar.grid(column=0, columnspan=6, row=0, sticky='nsew')

        # nav bar grid layout
        nav_bar.columnconfigure((0,1,2,3,4), weight=1, uniform='a')
        nav_bar.rowconfigure(0, weight=1, uniform='a')

        # A get request to the server
        url = "https://defnotturt.pythonanywhere.com/get_master_user/"
        params = {"id_user": self.user_id}

        connection = requests.get(url, params=params)
        response = connection.json()

        self.username = response[0][0]

        # widgets for nav bar
        ttk.Label(master = nav_bar, text=f'Welcome {self.username}!', bootstyle = 'SECONDARY').grid(row = 0, column = 2)
        ttk.Button(master = nav_bar, text='Log Out', bootstyle = 'DANGER', command = self.logout).grid(row = 0, column = 4, sticky='e', padx = 20)

    def create_password_field(self):
        password_frame = ttk.Frame(master=self)
        password_frame.grid(column=2, columnspan=4, row=1, rowspan=9, sticky='nsew')

        url = "https://defnotturt.pythonanywhere.com/select_all_pwd/"

        params = {"id_user": self.user_id}

        # A get request to the server
        connection = requests.get(url, params=params)
        response = connection.json()

        result = response.get('result')
        # TODO: result needs to be a list of tuples!

        if result:
            PasswordTable(master=password_frame, rowdata=result).pack()
        else:
            ttk.Label(master=password_frame, text="You have not yet stored any passwords").place(relx = 0.5, rely = 0.5, anchor='center')

        password_actions_frame = ttk.Frame(master=password_frame)
        password_actions_frame.pack(pady = 20)
        ttk.Button(master=password_actions_frame, text='ADD NEW', bootstyle = 'SUCCESS', command=self.add_password).pack(side = 'left', padx = 20)
        ttk.Button(master=password_actions_frame, text='UPDATE', bootstyle = 'WARNING', command=self.update_password).pack(side = 'left', padx = 20)
        ttk.Button(master=password_actions_frame, text='DELETE', bootstyle = 'DANGER', command=self.delete_password).pack(side = 'left', padx = 20)

    def create_generate_password_field(self):
        password_generate_frame = ttk.Frame(master=self)
        password_generate_frame.grid(column=0, row=1, rowspan=9, columnspan=2, sticky='nsew')

        self.password_textvar = tk.StringVar(value='')
        
        ttk.Label(master=password_generate_frame, text = 'Generate a password', bootstyle = 'SECONDARY').pack(side='top', pady = 10)
        ttk.Label(master=password_generate_frame, text='Password Length:', bootstyle='PRIMARY').pack(side='top', pady=10)
        self.scale = ttk.Scale(password_generate_frame, from_=8, to=20, length=100, bootstyle='PRIMARY', value=8, command=self.accept_whole_number_only)
        self.scale.pack(side='top', pady=10)
        self.pass_len_label = ttk.Label(master=password_generate_frame, bootstyle='PRIMARY', text='8 characters')
        self.pass_len_label.pack(side='top', pady=10)
        ttk.Entry(master=password_generate_frame, bootstyle='PRIMARY', textvariable=self.password_textvar).pack(side='top', pady=10)
        ttk.Button(master=password_generate_frame, text='Generate Password', bootstyle='SUCCESS', command=self.generate_password).pack(side='top', pady=10)

    def generate_password(self):
        length = round(self.scale.get())
        self.password_textvar.set(generate_password(length))

    # TODO: Do these methods!
    def add_password(self):
        pass

    def update_password(self):
        pass

    def delete_password(self):
        pass

    def logout(self):
        if self.main_window != None:
            self.destroy()
            self.update()
            self.main_window.deiconify()
        else:
            global app
            app.destroy()

    def accept_whole_number_only(self, e=None):
        value = self.scale.get()
        if int(value) != value:
            self.scale.set(round(value))
            self.pass_len_label.config(text=f'{round(value)} characters')


if __name__ == '__main__':
    app = ttk.Window()
    Home()
    app.mainloop()