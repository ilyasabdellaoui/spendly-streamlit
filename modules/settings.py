# modules/settings.py
import streamlit as st

def render_settings(data_manager) -> None:
    st.title("⚙️ Settings")
    
    st.header("Preferences")
    
    # Currency selector
    currencies = {
        "Dollar": "$",
        "Euro": "€",
        "Dirham": "DH",
        # Add more currencies as needed
    }

    # Get the user's default currency from session state
    default_currency_name = st.session_state.get("currency_name", "Euro")  # Fallback to "Euro"
    default_currency_symbol = st.session_state.get("currency_symbol", "€")  # Fallback to "€"

    # Find the key for the default currency
    default_currency_key = next(
        (key for key, symbol in currencies.items() if symbol == default_currency_symbol),
        "Euro"  # Fallback if no match is found
    )

    # Currency dropdown
    selected_currency = st.selectbox(
        "Select Currency",
        options=list(currencies.keys()),
        index=list(currencies.keys()).index(default_currency_key),  # Pre-select the user's currency
        format_func=lambda x: f"{x} ({currencies[x]})",
    )
    
    # Update session state with the selected currency
    st.session_state["currency_symbol"] = currencies[selected_currency]
    st.session_state["currency_name"] = selected_currency
    
    st.write(f"Selected currency: {st.session_state['currency_symbol']}")