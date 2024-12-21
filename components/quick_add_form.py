import streamlit as st
from datetime import datetime

def render_quick_add_form(data_manager) -> None:
    with st.form("quick_add", clear_on_submit=True):
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        col1, col2 = st.columns(2)
        with col1:
            op_type = st.selectbox("Type", ['expense', 'income'])
        with col2:
            category = st.selectbox(
                "Category", 
                ['Food', 'Transport', 'Housing', 'Entertainment', 'Utilities', 'Salary', 'Other']
            )
        
        if st.form_submit_button("Add Transaction", use_container_width=True):
            new_operation = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'description': description,
                'amount': amount,
                'type': op_type,
                'category': category
            }
            data_manager.add_operation(new_operation)
            st.success("Transaction added!")
            st.rerun()