import streamlit as st

def render_sidebar(data_manager) -> str:
    st.sidebar.title("Finance Manager 💰")
    selected = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "Operations", "Analytics", "Reports", "Settings"],
        index=0,
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Stats")

    currency_symbol = st.session_state.get("currency_symbol", "€")

    operations = data_manager.get_operations()
    if operations:
        import pandas as pd
        df = pd.DataFrame(operations)
        total_income = df[df['type'] == 'income']['amount'].sum()
        total_expenses = df[df['type'] == 'expense']['amount'].sum()
        st.sidebar.metric("Total Income", f"{total_income:,.2f}{currency_symbol}")
        st.sidebar.metric("Total Expenses", f"{total_expenses:,.2f}{currency_symbol}")
    
    return selected