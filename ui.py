import tkinter as tk
from add_edit import StudentAddEditPage
from auth import login_user, register_user, delete_user
from students_page import StudentsPage

class App:
    def __init__(self, root):
        self.root = root
        self.current_user = None

        self.login_frame = tk.Frame(root, bg="#0f172a")
        self.register_frame = tk.Frame(root, bg="#0f172a")

        self.build_login()
        self.build_register()

        self.login_frame.pack(fill="both", expand=True)

    # ================= TOAST =================
    def toast(self, msg, color="#ef4444"):
        t = tk.Label(self.root, text=msg,
                     bg=color, fg="white",
                     font=("Arial", 10, "bold"))
        t.place(relx=0.5, rely=0.95, anchor="center")
        self.root.after(2000, t.destroy)

    # ================= LOGIN UI =================
    def build_login(self):
        card = tk.Frame(self.login_frame, bg="#1e293b")
        card.place(relx=0.5, rely=0.5, anchor="center", width=320, height=260)

        tk.Label(card, text="Login", fg="white", bg="#1e293b",
                 font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(card, text="Username", fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=45)
        self.u = tk.Entry(card, width=30)
        self.u.pack(pady=(0, 10))
        self.u.bind("<Return>", lambda e: self.p.focus())

        tk.Label(card, text="Password", fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=45)
        self.p = tk.Entry(card, show="*", width=30)
        self.p.pack(pady=(0, 10))
        self.p.bind("<Return>", lambda e: self.login())

        tk.Button(card, text="Login", bg="#3b82f6", fg="white",
                  width=25,
                  command=self.login).pack(pady=10)

        tk.Button(card, text="Go Register", bg="#1e293b",
                  fg="#3b82f6", font=("Arial", 9),
                  command=self.show_register).pack()

    # ================= REGISTER UI =================
    def build_register(self):
        card = tk.Frame(self.register_frame, bg="#1e293b")
        card.place(relx=0.5, rely=0.5, anchor="center", width=320, height=260)

        tk.Label(card, text="Register", fg="white", bg="#1e293b",
                 font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(card, text="Username", fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=45)
        self.ru = tk.Entry(card, width=30)
        self.ru.pack(pady=(0, 10))
        self.ru.bind("<Return>", lambda e: self.rp.focus())

        tk.Label(card, text="Password", fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=45)
        self.rp = tk.Entry(card, show="*", width=30)
        self.rp.pack(pady=(0, 10))
        self.rp.bind("<Return>", lambda e: self.register())

        tk.Button(card, text="Create", bg="#10b981", fg="white",
                  width=25,
                  command=self.register).pack(pady=10)

        tk.Button(card, text="Back", bg="#1e293b",
                  fg="#3b82f6", font=("Arial", 9),
                  command=self.show_login).pack()

    # ================= LOGIN =================
    def login(self):
        u = self.u.get().strip()
        p = self.p.get().strip()

        if not u or not p:
            self.toast("Enter username & password ❌")
            return

        if login_user(u, p):
            self.current_user = u
            self.show_students()
        else:
            self.toast("Wrong username or password ❌")

    # ================= REGISTER =================
    def register(self):
        u = self.ru.get().strip()
        p = self.rp.get().strip()

        if not u or not p:
            self.toast("Fill all fields ❌")
            return

        if register_user(u, p):
            self.toast("Account created ✅", "#10b981")
            self.show_login()
        else:
            self.toast("User already exists ❌")

    # ================= SWITCH =================
    def show_login(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(fill="both", expand=True)

    # ================= LOGOUT =================
    def logout(self):
        self.current_user = None
        self.students_page.frame.destroy()
        self.login_frame.pack(fill="both", expand=True)

    # ================= DELETE ACCOUNT =================
    def delete_account(self):
        delete_user(self.current_user)
        self.logout()

        # ================= STUDENTS =================
    def show_students(self):
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()

        self.students_page = StudentsPage(self.root, self.current_user, self)
        
      




# ================= ADD/EDIT VIEW =================
    def show_add_edit(self, mode="add", index=None):
        self.students_page.frame.pack_forget()
        self.add_edit_page = StudentAddEditPage(self.root, self.students_page, mode, index)