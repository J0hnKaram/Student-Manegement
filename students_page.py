import tkinter as tk

class StudentsPage(tk.Frame):
    def __init__(self, root, user, app):
        super().__init__(root)

        self.root = root
        self.user = user
        self.app = app

        tk.Label(self, text=f"Students of {user}", font=("Arial", 16)).pack(pady=20)