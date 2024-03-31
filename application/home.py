import tkinter as tk
import ttkbootstrap as ttk
import requests

class Home(ttk.Toplevel):
    def __init__(self, last_window, user_id):
        # setup
        self.last_window = last_window
        super().__init__()
        self.user_id = user_id
        self.title('Home')
        self.geometry('800x600')
        self.minsize(width=800, height=400)

        # place widgets
        self.list_passwords()

        # bindings
        self.protocol("WM_DELETE_WINDOW", self.close_app)

        # mainloop
        self.mainloop()

    def close_app(self):
        self.last_window.destroy()

    def list_passwords(self):
        table = ttk.Treeview(
            self,
            columns = ('id_password', 'id_user', 'url', 'username', 'password'),
            show = 'headings'
        )
        table.heading('id_password', text = 'ID Password')
        table.heading('id_user', text = 'ID User')
        table.heading('url', text = 'Website URL')
        table.heading('username', text = 'Username/Email')
        table.heading('password', text = 'Password')
        table.pack(fill = 'both', expand = True)

        url = "https://turturicar.pythonanywhere.com/get_data/"

        # A get request to the server
        connection = requests.get(url)
        response = connection.json()

        if not response.get('error'):
            result = response.get('result')
            if result:
                for row in result:
                    table.insert(
                        parent='',
                        index=0,
                        values=list(row.values())
                    )
            else:
                # TODO: Add a label here!
                print("You have not yet stored any passwords!")
        else:
            print(response['error'])


