import streamlit as st
from pathlib import Path
from services.data_manager import DataManager, PostgresStorage
from components.sidebar import render_sidebar
import modules.dashboard as dashboard
import modules.operations as operations
import modules.analytics as analytics
import modules.reports as reports
import modules.settings as settings

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

# Initialize services
storage = PostgresStorage()
data_manager = DataManager(storage)

# Render sidebar and get selected page
selected_page = render_sidebar(data_manager)

# Render selected page
if selected_page == "Dashboard":
    dashboard.render_dashboard(data_manager)
elif selected_page == "Operations":
    operations.render_operations(data_manager)
elif selected_page == "Analytics":
    analytics.render_analytics(data_manager)
elif selected_page == "Reports":
    reports.render_reports(data_manager)
else:  # Settings
    settings.render_settings(data_manager)