# IMPORTANT!
# This file is only for testing
# This is a copy of home.py file that does not require server interaction

import tkinter as tk
import ttkbootstrap as ttk
from settings import *
from password_table import PasswordTable


class Home(ttk.Toplevel):
    def __init__(self, main_window=None, user_id=1):
        # setup
        self.main_window = main_window
        super().__init__()
        self.user_id = user_id
        self.title('Home')
        self.minsize(width=850, height=600)

        # grid layout
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1, uniform='a')

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

        # Widgets for nav bar
        ttk.Label(master=nav_bar, text='Welcome User!', bootstyle='SECONDARY').grid(row=0, column=2)
        ttk.Button(master=nav_bar, text='Log Out', bootstyle='DANGER', command=self.logout).grid(row=0, column=4, sticky='e', padx=20)

    def create_password_field(self):
        password_frame = ttk.Frame(master=self)
        password_frame.grid(column=2, columnspan=4, row=1, rowspan=9)

        ttk.Label(master=password_frame, text='List of Passwords:', bootstyle = 'PRIMARY', font=(FONT, TEXT_SIZE)).pack()

        # Hardcoded example data
        result = [
            ('example.com', 'user1', 'password1'),
            ('example.net', 'user2', 'password2'),
        ]

        self.result = result

        password_actions_frame = ttk.Frame(master=password_frame)

        if result:
            PasswordTable(master=password_frame, rowdata=result, use = 'show', user_id=self.user_id).pack(pady = 50)

            ttk.Button(master=password_actions_frame, text='ADD NEW', bootstyle = 'SUCCESS', command=self.add_password).pack(side = 'left', padx = 20)
            ttk.Button(master=password_actions_frame, text='UPDATE', bootstyle = 'WARNING', command=self.update_password).pack(side = 'left', padx = 20)
            ttk.Button(master=password_actions_frame, text='DELETE', bootstyle = 'DANGER', command=self.delete_password).pack(side = 'left', padx = 20)

        else:
            ttk.Label(master=password_frame, text="You have not yet stored any passwords").place(relx=0.5, rely=0.5, anchor='center')
            ttk.Button(master=password_actions_frame, text='ADD NEW', bootstyle = 'SUCCESS', command=self.add_password).pack(side = 'left', padx = 20)  
        
        password_actions_frame.pack(pady = 20)

    def create_generate_password_field(self):
        password_generate_frame = ttk.Frame(master=self)
        password_generate_frame.grid(column=0, row=1, rowspan=9, columnspan=2, sticky='nsew', padx = 20)

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

    def add_password(self):
        add_password_window = ttk.Toplevel()
        ttk.Label(master = add_password_window, text='Add a new password:', bootstyle = 'PRIMARY').pack(pady = 10)
        new_password_frame = ttk.Frame(master=add_password_window)
        new_password_frame.pack(pady = 20, padx = 20)
        ttk.Label(master=new_password_frame, text='Website:', bootstyle = 'PRIMARY').grid(row = 0, column=0, padx=10, pady=5)
        website_entry = ttk.Entry(master=new_password_frame, bootstyle = 'SECONDARY')
        website_entry.grid(row = 0, column=1, padx=10, pady=5)
        ttk.Label(master=new_password_frame, text='Username:', bootstyle = 'PRIMARY').grid(row = 1, column=0, padx=10, pady=5)
        username_entry = ttk.Entry(master=new_password_frame, bootstyle = 'SECONDARY')
        username_entry.grid(row = 1, column=1, padx=10, pady=5)
        ttk.Label(master=new_password_frame, text='Password:', bootstyle = 'PRIMARY').grid(row = 2, column=0, padx=10, pady=5)
        password_entry = ttk.Entry(master=new_password_frame, bootstyle = 'SECONDARY')
        password_entry.grid(row = 2, column=1, padx=10, pady=5)

        ttk.Button(
            master = add_password_window, 
            text='Add Password', 
            bootstyle = 'SUCCESS', 
            command=lambda: self.save_password(
                window=add_password_window, 
                user_entry=username_entry, 
                password_entry=password_entry, 
                website_entry=website_entry
            )
        ).pack(pady = 10)

    def save_password(self, window, user_entry, password_entry, website_entry):
        # NO SERVER INTERACTION FOR THIS FILE!

        # url = "https://defnotturt.pythonanywhere.com/store_pwd/"
        # username = user_entry.get()
        # password = password_entry.get()
        # website = website_entry.get()
        # params = {"id_user": self.user_id, "url_path": website, "username": username, "password": password}

        # connection = requests.post(url, params=params)
        # response = connection.json()

        window.destroy()

    def update_password(self):
        add_password_window = ttk.Toplevel()
        ttk.Label(master = add_password_window, text='Update a password:', bootstyle = 'PRIMARY').pack(pady = 10)

        PasswordTable(master=add_password_window, rowdata=self.result, use = 'update', user_id=self.user_id, window=add_password_window).pack()

    def delete_password(self):
        add_password_window = ttk.Toplevel()
        ttk.Label(master = add_password_window, text='Update a password:', bootstyle = 'PRIMARY').pack(pady = 10)

        PasswordTable(master=add_password_window, rowdata=self.result, use = 'delete', user_id=self.user_id, window=add_password_window).pack()

    def logout(self):
        if self.main_window:
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
