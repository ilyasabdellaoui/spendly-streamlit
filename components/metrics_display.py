import streamlit as st
import pandas as pd
from datetime import datetime

def render_key_metrics(data_manager, time_frame: str) -> None:
    operations = data_manager.get_operations()
    if not operations:
        return
    
    df = pd.DataFrame(operations)
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate period boundaries
    now = datetime.now()
    if time_frame == "Week":
        current_start = now - pd.DateOffset(weeks=1)
        previous_start = current_start - pd.DateOffset(weeks=1)
    elif time_frame == "Month":
        current_start = now - pd.DateOffset(months=1)
        previous_start = current_start - pd.DateOffset(months=1)
    elif time_frame == "Year":
        current_start = now - pd.DateOffset(years=1)
        previous_start = current_start - pd.DateOffset(years=1)
    
    # Calculate metrics for current period
    current_df = df[df['date'] >= current_start]
    current_income = current_df[current_df['type'] == 'income']['amount'].sum()
    current_expenses = current_df[current_df['type'] == 'expense']['amount'].sum()
    current_net = current_income - current_expenses
    
    # Calculate metrics for previous period
    previous_df = df[(df['date'] >= previous_start) & (df['date'] < current_start)]
    previous_income = previous_df[previous_df['type'] == 'income']['amount'].sum()
    previous_expenses = previous_df[previous_df['type'] == 'expense']['amount'].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_balance = data_manager.get_current_balance()
        st.metric(
            "Current Balance",
            f"${current_balance:,.2f}",
            delta=f"${current_net:,.2f} this {time_frame.lower()}"
        )
    
    with col2:
        expense_change = previous_expenses - current_expenses  # Note: reversed for intuitive display
        st.metric(
            f"{time_frame}'s Expenses",
            f"${current_expenses:,.2f}",
            delta=f"${expense_change:,.2f}",
            delta_color="inverse"  # Lower expenses are good
        )
    
    with col3:
        latest_transaction = current_df.iloc[-1] if not current_df.empty else None
        if latest_transaction is not None:
            amount = latest_transaction['amount']
            tx_type = latest_transaction['type']
            st.metric(
                "Latest Transaction",
                f"${amount:,.2f}",
                delta=tx_type.capitalize()
            )