# components/metrics_display.py
import streamlit as st
import pandas as pd

def get_period_label(start_date, end_date):
    delta_days = (end_date - start_date).days
    
    if delta_days == 0:
        return "today"
    elif delta_days == 1:
        return "this day"
    elif delta_days == 7:
        return "this week"
    elif delta_days in [28, 29, 30, 31]:
        return "this month"
    elif delta_days in [90, 91, 92]:
        return "this quarter"
    elif delta_days in [365, 366]:
        return "this year"
    else:
        return f"these {delta_days} days"

def render_key_metrics(data_manager, start_date, end_date) -> None:
    operations = data_manager.get_operations()
    if not operations:
        return

    df = pd.DataFrame(operations)
    df['entry_date'] = pd.to_datetime(df['entry_date'])  # Use 'entry_date' instead of 'date'

    # Ensure dates are datetime objects
    current_start = pd.to_datetime(start_date)
    current_end = pd.to_datetime(end_date)
    
    # Calculate previous period
    period_length = (current_end - current_start)
    previous_start = current_start - period_length
    previous_end = current_start

    current_df = df[(df['entry_date'] >= current_start) & (df['entry_date'] <= current_end)]
    current_income = current_df[current_df['type'] == 'income']['amount'].sum()
    current_expenses = current_df[current_df['type'] == 'expense']['amount'].sum()
    current_net = current_income - current_expenses

    previous_df = df[(df['entry_date'] >= previous_start) & (df['entry_date'] < previous_end)]
    previous_expenses = previous_df[previous_df['type'] == 'expense']['amount'].sum()

    # Get dynamic period label
    period_label = get_period_label(current_start, current_end)
    currency_symbol = st.session_state.get("currency_symbol", "€")

    col1, col2, col3 = st.columns(3)

    with col1:
        current_balance = data_manager.get_current_balance()
        if current_net > 0:
            st.metric(
                "Current Balance",
                f"{current_balance:,.2f}{currency_symbol}",
                delta=f"{current_net:,.2f} {period_label}{currency_symbol}",
                delta_color="normal"
            )
        else:
            st.metric(
                "Current Balance",
                f"{current_balance:,.2f}{currency_symbol}",
                delta=f"{current_net:,.2f} {period_label}{currency_symbol}",
                delta_color="inverse"
            )

    with col2:
        expense_change = -abs(previous_expenses - current_expenses)
        st.metric(
            "Period Expenses",
            f"{current_expenses:,.2f}{currency_symbol}",
            delta=f"{expense_change:,.2f}{currency_symbol}",
            delta_color="inverse"
        )

    with col3:
        latest_transaction = current_df.iloc[-1] if not current_df.empty else None
        if latest_transaction is not None:
            tx_type = latest_transaction['type']
            delta_color = "normal" if tx_type == "income" else "off"
            amount = -latest_transaction['amount'] if tx_type == "expense" else latest_transaction['amount']
            st.metric(
                "Latest Transaction",
                f"{amount:,.2f}{currency_symbol}",
                delta=tx_type.capitalize(),
                delta_color=delta_color
            )