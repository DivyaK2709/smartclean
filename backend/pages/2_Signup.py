# pages/2_Signup.py
import streamlit as st
from database import create_user, find_user_by_username
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

st.set_page_config(page_title="Signup - SmartClean")
st.title("Create an account")

username = st.text_input("Choose a username")
password = st.text_input("Choose a password", type="password")
msg = st.empty()

if st.button("Create Account"):
    if not username or not password:
        msg.error("Enter username and password")
    else:
        if find_user_by_username(username):
            msg.error("Username already exists")
        else:
            hashed = pwd_context.hash(password)
            uid = create_user(username, hashed)
            msg.success("Account created. Please login.")
