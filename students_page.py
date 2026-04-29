import tkinter as tk
from tkinter import ttk
from storage import load_students, save_students

class StudentsPage:
    def __init__(self, root, username, app_instance):
        self.root = root
        self.username = username
        self.app = app_instance
        
        self.all_data = load_students()
        self.students = self.all_data.get(self.username, [])

        self.frame = tk.Frame(self.root, bg="#0f172a")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text=f"Welcome, {username}", 
                 fg="white", bg="#0f172a", font=("Arial", 16, "bold")).pack(pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e293b", foreground="white", fieldbackground="#1e293b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#3b82f6')])

        columns = ("name", "year", "birth", "subjects", "avg")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("name", text="Student Name")
        self.tree.heading("year", text="Academic Year")
        self.tree.heading("birth", text="Birth Date")
        self.tree.heading("subjects", text="Subjects Count")
        self.tree.heading("avg", text="Average Grade")

        for col in columns:
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="x")

        btn_frame = tk.Frame(self.frame, bg="#0f172a")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="➕ Add New Student", bg="#10b981", fg="white", 
                  font=("Arial", 10, "bold"), command=self.add_student).pack(side="left", padx=10, ipadx=10, ipady=5)
        
        tk.Button(btn_frame, text="📝 Edit Selected", bg="#3b82f6", fg="white", 
                  font=("Arial", 10, "bold"), command=self.edit_student).pack(side="left", padx=10, ipadx=10, ipady=5)
        
        tk.Button(btn_frame, text="🗑️ Delete Selected", bg="#ef4444", fg="white", 
                  font=("Arial", 10, "bold"), command=self.delete_student).pack(side="left", padx=10, ipadx=10, ipady=5)
        
        tk.Button(btn_frame, text="🔄 Refresh", bg="#6366f1", fg="white", 
                  font=("Arial", 10, "bold"), command=self.load_and_refresh).pack(side="left", padx=10, ipadx=10, ipady=5)

        tk.Button(btn_frame, text="� Logout", bg="#ef4444", fg="white", 
                  font=("Arial", 10, "bold"), command=self.app.logout).pack(side="left", padx=10, ipadx=10, ipady=5)

        tk.Button(self.frame, text="⚠️ Delete My Account", bg="#475569", fg="white", 
                  command=self.app.delete_account).pack(side="bottom", pady=20)

        self.refresh()

    def load_and_refresh(self):
        self.all_data = load_students()
        self.students = self.all_data.get(self.username, [])
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for i, s in enumerate(self.students):
            subs = s.get("subjects", [])
            avg = sum(item['score'] for item in subs) / len(subs) if subs else 0
            self.tree.insert("", "end", iid=i, values=(s["name"], s["year"], s["birth"], len(subs), f"{avg:.1f}"))

    def save(self):
        self.all_data[self.username] = self.students
        save_students(self.all_data)

    def add_student(self):
        self.app.show_add_edit(mode="add")

    def edit_student(self):
        selection = self.tree.selection()
        if selection:
            index = int(selection[0])
            self.app.show_add_edit(mode="edit", index=index)

    def delete_student(self):
        selection = self.tree.selection()
        if not selection:
            self.app.toast("Please select a student to delete ❌")
            return

        index = int(selection[0])
        student_name = self.students[index]["name"]

        # إنشاء نافذة تأكيد مخصصة (Custom Modal)
        dialog = tk.Toplevel(self.root)
        dialog.title("Confirm Delete")
        dialog.geometry("350x200")
        dialog.configure(bg="#1e293b")
        dialog.resizable(False, False)
        dialog.transient(self.root)  # تجعلها مرتبطة بالنافذة الرئيسية
        dialog.grab_set()             # تمنع التفاعل مع النافذة الخلفية حتى تغلق

        # وضع النافذة في منتصف التطبيق
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 175
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 100
        dialog.geometry(f"+{int(x)}+{int(y)}")

        tk.Label(dialog, text="⚠️", font=("Arial", 30), bg="#1e293b", fg="#ef4444").pack(pady=(15, 0))
        tk.Label(dialog, text=f"Delete '{student_name}'?", font=("Arial", 12, "bold"), bg="#1e293b", fg="white").pack(pady=5)
        tk.Label(dialog, text="This action cannot be undone.", font=("Arial", 9), bg="#1e293b", fg="#94a3b8").pack()

        btn_container = tk.Frame(dialog, bg="#1e293b")
        btn_container.pack(pady=20)

        def on_confirm():
            del self.students[index]
            self.save()
            self.refresh()
            self.app.toast(f"{student_name} deleted ✅", "#10b981")
            dialog.destroy()

        tk.Button(btn_container, text="Delete", bg="#ef4444", fg="white", width=12, font=("Arial", 9, "bold"), command=on_confirm).pack(side="left", padx=10)
        tk.Button(btn_container, text="Cancel", bg="#475569", fg="white", width=12, font=("Arial", 9, "bold"), command=dialog.destroy).pack(side="left", padx=10)