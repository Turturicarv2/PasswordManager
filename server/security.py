from hashlib import sha256

def hash_password(password):
    m = sha256()
    m.update(password.encode('utf-8'))
    return m.hexdigest()