import tkinter as tk
import ttkbootstrap as ttk
import requests
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

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
        if self.main_window != None:
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

        if result:
            coldata = ["url", "username", "password"]
            dt = Tableview(
                master=app,
                coldata=coldata,
                paginated=True,
                searchable=True,
                bootstyle=PRIMARY,
            )
            dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

            for row in result:
                dt.insert_row('end', list(row.values()))
        else:
            ttk.Label(master=password_frame, text="You have not yet stored any passwords").place(relx = 0.5, rely = 0.5, anchor='center')

    def create_generate_password_field(self):
        password_generate_frame = ttk.Frame(master=self)
        password_generate_frame.grid(column=0, row=1, rowspan=9, columnspan=2, sticky='nsew')

        pass_length = ttk.IntVar()

        ttk.Label(master = password_generate_frame, text='Password Length:', bootstyle = 'PRIMARY').pack(side = 'top', pady = 10)
        self.scale = ttk.Scale(password_generate_frame, from_ = 8, to = 21, length = 100, variable = pass_length, bootstyle = 'PRIMARY', value = 8, command = self.accept_whole_number_only)
        self.scale.pack(side = 'top', pady=10)
        self.pass_len_label = ttk.Label(master=password_generate_frame, bootstyle = 'PRIMARY', text = '8 characters')
        self.pass_len_label.pack(side = 'top', pady=10)
        ttk.Entry(master=password_generate_frame, bootstyle = 'PRIMARY').pack(side = 'top', pady = 10, padx=10)
        ttk.Button(master=password_generate_frame, text='Generate Password', bootstyle = 'SUCCESS').pack(side = 'top', pady = 10)

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
            self.pass_len_label.config(text=f'{int(value)} characters')


if __name__ == '__main__':
    app = ttk.Window()
    Home()
    app.mainloop()