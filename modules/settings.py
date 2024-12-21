import streamlit as st

def render_settings(data_manager) -> None:
    st.title("⚙️ Settings")
    
    st.header("Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Reset All Data", type="primary"):
            data_manager.clear_data()
            st.success("All data has been reset!")
            st.rerun()
