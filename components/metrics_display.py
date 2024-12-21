import streamlit as st
import pandas as pd
from datetime import datetime

def render_key_metrics(data_manager, time_frame: str) -> None:
    operations = data_manager.get_operations()
    if not operations:
        return
    
    df = pd.DataFrame(operations)
    df['date'] = pd.to_datetime(df['date'])
    
    # Filter based on time frame
    if time_frame == "Week":
        start_date = datetime.now() - pd.DateOffset(weeks=1)
    elif time_frame == "Month":
        start_date = datetime.now() - pd.DateOffset(months=1)
    elif time_frame == "Year":
        start_date = datetime.now() - pd.DateOffset(years=1)
    else:  # All Time
        start_date = df['date'].min()
    
    filtered_df = df[df['date'] >= start_date]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        current_balance = data_manager.get_current_balance()
        st.metric(
            "Current Balance",
            f"${current_balance:,.2f}",
            delta=f"${current_balance - (filtered_df[filtered_df['type'] == 'expense']['amount'].sum() if not filtered_df.empty else 0):,.2f}"
        )
    
    with col2:
        current_expenses = filtered_df[filtered_df['type'] == 'expense']['amount'].sum()
        last_expenses = df[df['date'] < start_date][df['type'] == 'expense']['amount'].sum()
        delta = current_expenses - last_expenses
        st.metric(
            f"{time_frame}'s Expenses",
            f"${current_expenses:,.2f}",
            delta=f"${delta:,.2f} vs previous period"
        )
    
    with col3:
        if not filtered_df.empty:
            recent_balance_change = filtered_df.iloc[-1]['amount']
            change_type = "+" if filtered_df.iloc[-1]['type'] == 'income' else "-"
            st.metric(
                "Latest Transaction",
                f"${recent_balance_change:,.2f}",
                delta=f"{change_type}${recent_balance_change:,.2f}"
            )