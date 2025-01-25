# modules/login.py
import streamlit as st
from services.api_manager import APIStorage

def render_login(storage: APIStorage):
    """Render the full-page login form."""
    st.markdown(
        """
        <style>
        /* Center the login form */
        .stLogin {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
        }

        /* Input fields */
        .stTextInput input, .stTextInput input:focus {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            outline: none;
            box-shadow: none;
        }

        /* Login button */
        .stButton button {
            width: 100%;
            padding: 0.75rem;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .stButton button:hover {
            background-color: #45a049;
        }

        /* Error message */
        .stError {
            color: #ff4b4b;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }

        /* Loading spinner */
        .stSpinner {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Login form container
    st.markdown("<div class='stLogin'>", unsafe_allow_html=True)

    # Title
    st.markdown("<h1 style='text-align: center; margin-bottom: 1.5rem;'>🔑 Login</h1>", unsafe_allow_html=True)

    # Username and password fields
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    # Login button
    if st.button("Login"):
        if not username or not password:
            st.error("Please fill in both username and password.")
        else:
            with st.spinner("Logging in..."):  # Show loading spinner
                if storage.login(username, password):
                    st.success("Logged in successfully!")
                    st.session_state["logged_in"] = True
                    st.rerun()  # Rerun to update the app
                else:
                    st.error("Invalid username or password.")

    st.markdown("</div>", unsafe_allow_html=True)