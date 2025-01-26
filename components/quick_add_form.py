# components/quick_add_form.py
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
            # Get categories from database
            categories = data_manager.get_categories()
            default_categories = ['Food', 'Transport', 'Housing', 'Entertainment', 'Utilities', 'Salary', 'Other']
            category_list = categories if categories else default_categories
            category = st.selectbox("Category", category_list)
        
        if st.form_submit_button("Add Transaction", use_container_width=True):
            try:
                new_operation = {
                    'entry_date': datetime.now().strftime('%Y-%m-%d'),
                    'description': description,
                    'amount': amount,
                    'type': op_type,
                    'category': category
                }
                data_manager.add_operation(new_operation)
                st.success("Transaction added!")
                st.rerun()
            except Exception as e:
                st.error(f"Error adding transaction: {str(e)}")