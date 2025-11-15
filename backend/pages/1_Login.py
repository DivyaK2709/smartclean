# pages/1_Login.py
import streamlit as st
from database import find_user_by_username
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

st.set_page_config(page_title="Login - SmartClean")
st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
msg = st.empty()

if st.button("Login"):
    if not username or not password:
        msg.error("Enter username and password")
    else:
        user = find_user_by_username(username)
        if not user:
            msg.error("User not found. Please signup.")
        else:
            hashed = user.get("password_hash") or user.get("hashed_password")
            try:
                ok = pwd_context.verify(password, hashed)
            except Exception:
                ok = False
            if ok:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                msg.success("Logged in. Go to Upload or Map.")
            else:
                msg.error("Invalid credentials")
