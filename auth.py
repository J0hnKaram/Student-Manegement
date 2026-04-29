from storage import load_users, save_users, load_students, save_students
from utils import hash_password

# ================= REGISTER =================
def register_user(u, p):
    users = load_users()

    if u in users:
        return False

    users[u] = hash_password(p)
    save_users(users)
    return True

# ================= LOGIN =================
def login_user(u, p):
    users = load_users()
    return u in users and users[u] == hash_password(p)

# ================= DELETE =================
def delete_user(u):
    users = load_users()
    if u in users:
        del users[u]
        save_users(users)

        students = load_students()
        if u in students:
            del students[u]
            save_students(students)
            
        return True

    return False