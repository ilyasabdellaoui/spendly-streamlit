# components/sidebar.py
import streamlit as st

def render_sidebar(data_manager) -> str:
    st.sidebar.title("Finance Manager 💰")
    
    # Navigation options
    pages = ["Dashboard", "Operations", "Analytics", "Reports", "Settings", "Login"]
    selected = st.sidebar.radio(
        "Navigate",
        pages,
        index=0,
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Stats")

    currency_symbol = st.session_state.get("currency_symbol", "€")  # Default to "€" if not set

    try:
        operations = data_manager.get_operations()
        if operations:
            import pandas as pd
            df = pd.DataFrame(operations)
            total_income = df[df['type'] == 'income']['amount'].sum()
            total_expenses = df[df['type'] == 'expense']['amount'].sum()
            st.sidebar.metric("Total Income", f"{total_income:,.2f}{currency_symbol}")
            st.sidebar.metric("Total Expenses", f"{total_expenses:,.2f}{currency_symbol}")
    except Exception as e:
        st.sidebar.error("Failed to fetch operations. Please try again.")
        print(f"Error fetching operations: {e}")
    
    # Logout button (only show if logged in)
    if st.session_state.get("logged_in"):
        if st.sidebar.button("Logout"):
            st.session_state.clear()  # Clear all session state
            st.rerun()
    
    return selected.lower()  # Ensure the page name matches the routing logic