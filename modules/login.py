# modules/login.py
import streamlit as st
from services.api_manager import APIStorage

def render_login(storage: APIStorage):
    """Render the login page."""
    st.title("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if storage.login(username, password):
            st.success("Logged in successfully!")
            st.rerun()  # Rerun to update the app
        else:
            st.error("Invalid username or password.")