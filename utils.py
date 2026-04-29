import hashlib

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()
