import tkinter as tk
from ui import App

root = tk.Tk()
root.title("Student System")
root.geometry("900x600")
root.configure(bg="#0f172a")

App(root)

root.mainloop()