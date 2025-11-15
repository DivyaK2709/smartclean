# app.py
import streamlit as st

st.set_page_config(page_title="SmartClean", layout="wide", initial_sidebar_state="auto")

st.markdown(
    """
    <div style="display:flex;align-items:center;gap:16px">
      <img src="https://raw.githubusercontent.com/yourname/placeholder/main/logo.png" width="64" style="border-radius:12px"/>
      <div>
        <h2 style="margin:0">SmartClean</h2>
        <div style="color:gray;margin-top:-6px">Crowd-powered AI litter mapping — Streamlit edition</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Use the pages (left) to Login, Signup, Upload and view Map.")
st.write("If you are new, go to Signup → Login → Upload → Map.")
