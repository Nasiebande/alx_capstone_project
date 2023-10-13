# auth.py

import bcrypt

def register_user(username, password, users):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    users[username] = {'password': hashed_password}

def verify_password(username, password, users):
    if username in users:
        stored_password = users[username]['password']
        return bcrypt.checkpw(password.encode('utf-8'), stored_password)
    return False