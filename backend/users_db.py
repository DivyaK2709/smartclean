# users_db.py
from backend.database import create_user_doc, find_user
def create_user(username, hashed_password):
    return create_user_doc(username, hashed_password)

def find_user_by_username(username):
    return find_user(username)
