import streamlit as st
import pandas as pd
from datetime import datetime

def render_operations(data_manager) -> None:
    st.title("💼 Operations Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Upload CSV", "All Operations", "Search", "Edit"])
    
    with tab1:
        st.subheader("Upload Operations CSV")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            df_upload = pd.read_csv(uploaded_file)
            required_columns = ['Date', 'Operation', 'Category', 'Amount Deducted', 'Gains', 'Balance', 'Month']
            
            if all(col in df_upload.columns for col in required_columns):
                for _, row in df_upload.iterrows():
                    date_str = row['Date']
                    operation = row['Operation']
                    category = row['Category']
                    amount_deducted = float(row['Amount Deducted'])
                    gains = float(row['Gains'])
                    
                    op_type = 'expense' if amount_deducted < 0 else 'income' if gains > 0 else None
                    if op_type:
                        new_operation = {
                            'date': datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d'),
                            'description': operation,
                            'amount': abs(amount_deducted) if op_type == 'expense' else gains,
                            'type': op_type,
                            'category': category
                        }
                        data_manager.add_operation(new_operation)
                st.success("Operations added successfully!")
            else:
                st.error("Uploaded CSV must contain the following columns: " + ", ".join(required_columns))

    with tab2:
        operations = data_manager.get_operations()
        if operations:
            df = pd.DataFrame(operations)
            df['date'] = pd.to_datetime(df['date'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                date_range = st.date_input(
                    "Date Range",
                    [df['date'].min(), df['date'].max()]
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
                (df['date'].dt.date >= date_range[0]) &
                (df['date'].dt.date <= date_range[1]) &
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
                        format="$%.2f"
                    ),
                    "type": "Type",
                    "category": "Category"
                },
                hide_index=True
            )
    
    with tab3:
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
    
    with tab4:
        operations = data_manager.get_operations()
        if operations:
            df = pd.DataFrame(operations)
            selected_index = st.selectbox(
                "Select operation to edit/delete",
                range(len(df)),
                format_func=lambda x: f"{df.iloc[x]['date']} - {df.iloc[x]['description']} (${df.iloc[x]['amount']:,.2f})"
            )
            
            if st.button("🗑️ Delete Operation", type="primary"):
                data_manager.delete_operation(selected_index)
                st.success("Operation deleted successfully!")
                st.rerun()