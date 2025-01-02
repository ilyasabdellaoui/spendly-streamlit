# modules/settings.py
import streamlit as st

def render_settings(data_manager) -> None:
    st.title("⚙️ Settings")
    
    st.header("Preferences")
    
    # Currency selector
    currencies = {"Dollar": "$", "Euro": "€", "Dirham": "DH"}
    selected_currency = st.selectbox(
        "Select Currency",
        options=list(currencies.keys()),
        format_func=lambda x: f"{x} ({currencies[x]})",
    )
    
    # Update session state
    if "currency_symbol" not in st.session_state:
        st.session_state["currency_symbol"] = currencies[selected_currency]
    else:
        st.session_state["currency_symbol"] = currencies[selected_currency]
    
    st.write(f"Selected currency: {st.session_state['currency_symbol']}")
    
    st.header("Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Reset All Data", type="primary"):
            data_manager.clear_data()
            st.success("All data has been reset!")
            st.rerun()