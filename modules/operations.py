import streamlit as st
import pandas as pd
from datetime import datetime

def render_operations(data_manager) -> None:
    st.title("💼 Operations Management")

    currency_symbol = st.session_state.get("currency_symbol", "€")
    
    tab1, tab2, tab3 = st.tabs(["All Operations", "Search", "Edit"])
    
    with tab1:
        operations = data_manager.get_operations()
        if operations:
            df = pd.DataFrame(operations)
            df['entry_date'] = pd.to_datetime(df['entry_date'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                date_range = st.date_input(
                    "Date Range",
                    [df['entry_date'].min(), df['entry_date'].max()]
                )
            with col2:
                type_filter = st.multiselect(
                    "Type",
                    options=['income', 'expense'],
                    default=['income', 'expense']
                )
            with col3:
                category_filter = st.multiselect(
                    "Category",
                    options=df['category'].unique(),
                    default=df['category'].unique()
                )
            
            mask = (
                (df['entry_date'].dt.date >= date_range[0]) &
                (df['entry_date'].dt.date <= date_range[1]) &
                (df['type'].isin(type_filter)) &
                (df['category'].isin(category_filter))
            )
            filtered_df = df[mask]
            
            st.dataframe(
                filtered_df,
                column_config={
                    "date": "Date",
                    "description": "Description",
                    "amount": st.column_config.NumberColumn(
                        "Amount",
                        format=f"%.2f{currency_symbol}"
                    ),
                    "type": "Type",
                    "category": "Category"
                },
                hide_index=True
            )
    
    with tab2:
        search_term = st.text_input("🔍 Search operations", placeholder="Enter description...")
        if search_term:
            operations = data_manager.get_operations()
            if operations:
                df = pd.DataFrame(operations)
                results = df[df['description'].str.contains(search_term, case=False)]
                if not results.empty:
                    st.dataframe(results, hide_index=True)
                else:
                    st.info("No matching operations found.")
    
    with tab3:
        operations = data_manager.get_operations()
        if operations:
            df = pd.DataFrame(operations)
            selected_index = st.selectbox(
                "Select operation to edit/delete",
                range(len(df)),
                format_func=lambda x: f"{df.iloc[x]['entry_date']} - {df.iloc[x]['description']} ({df.iloc[x]['amount']:,.2f}{currency_symbol})"
            )
            
            if st.button("🗑️ Delete Operation", type="primary"):
                data_manager.delete_operation(selected_index)
                st.success("Operation deleted successfully!")
                st.rerun()