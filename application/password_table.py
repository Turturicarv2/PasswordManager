import ttkbootstrap as ttk
import tkinter as tk
import pyperclip

class PasswordTable(tk.Frame):
    def __init__(self, master=None, rowdata=None, use=None):
        self.use = use
        super().__init__(master)
        
        # Column headers
        ttk.Label(self, text="Website").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self, text="Username").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self, text="Password").grid(row=0, column=2, padx=5, pady=5)
        
        for i, data in enumerate(rowdata, start=1):
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
                ttk.Button(self, text='Update', bootstyle = 'WARNING', command=lambda: self.update_password()).grid(row = i, column=4, padx=5, pady=5)

            if self.use == 'delete':
                ttk.Button(self, text='Delete', bootstyle = 'DANGER', command=lambda: self.delete_password()).grid(row = i, column=4, padx=5, pady=5)
                
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

    # TODO: Add implementation
    def update_password(self):
        pass

    def delete_password(self):
        pass