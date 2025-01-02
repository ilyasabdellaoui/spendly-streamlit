# app.py
import streamlit as st
import os
from pathlib import Path
from services.data_manager import DataManager
from services.api_manager import APIStorage
from components.sidebar import render_sidebar
import modules.dashboard as dashboard
import modules.operations as operations
import modules.analytics as analytics
import modules.reports as reports
import modules.settings as settings
import modules.login as login
from dotenv import load_dotenv

# Page config
st.set_page_config(
    page_title="Spendly - Your Personal Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_path = Path("assets/style.css")
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load spendly api endpoint
load_dotenv()
API_URL = os.getenv('API_URL')

# Initialize services
storage = APIStorage(base_url=API_URL)
data_manager = DataManager(storage)

# Initialize session state for authentication
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Centralized routing logic
selected_page = render_sidebar(data_manager)

# Render the selected page
if selected_page == "login":
    login.render_login(storage)
elif selected_page == "dashboard":
    dashboard.render_dashboard(data_manager)
elif selected_page == "operations":
    operations.render_operations(data_manager)
elif selected_page == "analytics":
    analytics.render_analytics(data_manager)
elif selected_page == "reports":
    reports.render_reports(data_manager)
elif selected_page == "settings":
    settings.render_settings(data_manager)