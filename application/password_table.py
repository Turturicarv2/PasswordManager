import ttkbootstrap as ttk
import tkinter as tk
import pyperclip
import requests
from settings import *

class PasswordTable(tk.Frame):
    def __init__(self, master=None, rowdata=None, use=None, user_id = 1, window = None):
        # setup
        self.use = use
        self.user_id = user_id
        self.window = window
        super().__init__(master)

        processed_list = [sublist[2:] for sublist in rowdata]
        id_list = [sublist[0] for sublist in rowdata]
        
        # Column headers
        ttk.Label(self, text="Website").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self, text="Username").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self, text="Password").grid(row=0, column=2, padx=5, pady=5)
        
        for i, data in enumerate(processed_list, start=1):
            website, username, password = data
            
            # Website label
            ttk.Label(self, text=website).grid(row=i, column=0, padx=5, pady=5)
            
            # Username entry
            username_entry = ttk.Entry(self)
            username_entry.insert(0, username)
            if self.use != 'update':
                username_entry.configure(state='readonly')
            username_entry.grid(row=i, column=1, padx=5, pady=5)
            
            # Password entry
            password_entry = ttk.Entry(self)
            password_entry.insert(0, password)
            password_entry.configure(state='readonly')
            password_entry.grid(row=i, column=2, padx=5, pady=5)

            # Hide the password
            self.toggle_password_visibility(password_entry)
            
            # Button to toggle password visibility
            ttk.Button(self, text="Show/Hide", bootstyle = 'PRIMARY', command=lambda entry=password_entry: self.toggle_password_visibility(entry)).grid(row=i, column=3, padx=5, pady=5)

            if self.use == 'show':
                # Button to copy password to clipboard
                ttk.Button(self, text="Copy", bootstyle = 'PRIMARY', command=lambda password=password: self.copy_to_clipboard(password)).grid(row=i, column=4, padx=5, pady=5)

            if self.use == 'update':
                ttk.Button(self, text='Update', bootstyle = 'WARNING', command=lambda: self.update_password(user_entry = username_entry, password_entry = password_entry, password_id=id_list[i-1])).grid(row = i, column=4, padx=5, pady=5)

            if self.use == 'delete':
                ttk.Button(self, text='Delete', bootstyle = 'DANGER', command=lambda: self.delete_password(password_id=id_list[i-1])).grid(row = i, column=4, padx=5, pady=5)
                
    def toggle_password_visibility(self, entry: ttk.Entry):
        current_show = entry.cget("show")
        if current_show == "":
            entry.configure(show="•")  # Hide password
            if self.use == 'update':
                entry.configure(state = 'readonly')
        else:
            entry.configure(show="")   # Show password
            if self.use == 'update':
                entry.configure(state = 'normal')
            
    def copy_to_clipboard(self, password):  
        pyperclip.copy(password)

    def update_password(self, user_entry: ttk.Entry, password_entry: ttk.Entry, password_id):
        url = server_url + "update_pwd/"
        username = user_entry.get()
        password = password_entry.get()
        params = {"username": username, "password": password, "password_id": password_id}

        connection = requests.put(url, params=params)
        response = connection.json()

        # TODO: Add success/failure message 
        if response['success']:
            self.window.destroy()
        else:
            pass

    def delete_password(self, password_id):
        url = server_url + "delete_pwd/"
        params = {"password_id": password_id}

        connection = requests.delete(url, params=params)
        response = connection.json()

        # TODO: Add success/failure message 
        if response['success']:
            self.window.destroy()
        else:
            pass