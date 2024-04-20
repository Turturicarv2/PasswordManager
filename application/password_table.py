import ttkbootstrap as ttk
import tkinter as tk
import pyperclip

class PasswordTable(tk.Frame):
    def __init__(self, master=None, rowdata=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        # Column headers
        ttk.Label(self, text="Website").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self, text="Username").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self, text="Password").grid(row=0, column=2, padx=5, pady=5)
        
        self.password_entries = []
        
        for i, data in enumerate(rowdata, start=1):
            website, username, password = data
            
            # Website label
            ttk.Label(self, text=website).grid(row=i, column=0, padx=5, pady=5)
            
            # Username entry
            username_entry = ttk.Entry(self)
            username_entry.insert(0, username)
            username_entry.configure(state='readonly')
            username_entry.grid(row=i, column=1, padx=5, pady=5)
            
            # Password entry
            password_entry = ttk.Entry(self)
            password_entry.insert(0, password)
            password_entry.configure(state='readonly')
            password_entry.grid(row=i, column=2, padx=5, pady=5)

            # Hide the password
            self.toggle_password_visibility(password_entry) 
            
            # Store password entry for later use
            self.password_entries.append(password_entry)
            
            # Button to toggle password visibility
            toggle_button = ttk.Button(self, text="Show", command=lambda entry=password_entry: self.toggle_password_visibility(entry))
            toggle_button.grid(row=i, column=3, padx=5, pady=5)

            # Button to copy password to clipboard
            copy_button = ttk.Button(self, text="Copy", command=lambda password=password: self.copy_to_clipboard(password))
            copy_button.grid(row=i, column=4, padx=5, pady=5)
                
    def toggle_password_visibility(self, entry: ttk.Entry):
        current_show = entry.cget("show")
        if current_show == "":
            entry.configure(show="•")  # Show password
        else:
            entry.configure(show="")   # Hide password
            
    def copy_to_clipboard(self, password):  
        pyperclip.copy(password)