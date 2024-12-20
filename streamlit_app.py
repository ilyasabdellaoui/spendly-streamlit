import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Personal Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
        }
        .reportview-container {
            margin-top: -2rem;
        }
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        div[data-testid="stToolbar"] {visibility: hidden;}
        div[data-testid="stDecoration"] {visibility: hidden;}
        div[data-testid="stStatusWidget"] {visibility: hidden;}
        #stDateInput>div>div>input {text-align: left;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'operations' not in st.session_state:
    st.session_state.operations = []
if 'current_balance' not in st.session_state:
    st.session_state.current_balance = 0.0
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# Helper functions
def load_data():
    data_file = Path('operations.json')
    if data_file.exists():
        try:
            with open(data_file, 'r') as f:
                st.session_state.operations = json.load(f)
            calculate_balance()
        except json.JSONDecodeError:
            st.warning("Data file is corrupted. Starting with empty operations.")
            st.session_state.operations = []

def save_data():
    with open('operations.json', 'w') as f:
        json.dump(st.session_state.operations, f)

def calculate_balance():
    balance = 0
    for op in st.session_state.operations:
        if op['type'] == 'income':
            balance += op['amount']
        else:
            balance -= op['amount']
    st.session_state.current_balance = balance

# Load data at startup
load_data()

# Sidebar Navigation
st.sidebar.title("Finance Manager 💰")
selected = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Operations", "Analytics", "Reports", "Settings"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")
if st.session_state.operations:
    df = pd.DataFrame(st.session_state.operations)
    total_income = df[df['type'] == 'income']['amount'].sum()
    total_expenses = df[df['type'] == 'expense']['amount'].sum()
    st.sidebar.metric("Total Income", f"${total_income:,.2f}")
    st.sidebar.metric("Total Expenses", f"${total_expenses:,.2f}")

# Dashboard
if selected == "Dashboard":
    st.title("📊 Financial Dashboard")
    
    # Time Frame Selector
    time_frame = st.selectbox("Select Time Frame", ["Week", "Month", "Year", "All Time"])
    
    # Filter DataFrame Based on Time Frame
    if time_frame == "Week":
        start_date = datetime.now() - pd.DateOffset(weeks=1)
    elif time_frame == "Month":
        start_date = datetime.now() - pd.DateOffset(months=1)
    elif time_frame == "Year":
        start_date = datetime.now() - pd.DateOffset(years=1)
    else:  # All Time
        start_date = df['date'].min()

    filtered_df = df[pd.to_datetime(df['date']) >= start_date]

    # Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        current_balance = st.session_state.current_balance
        st.metric(
            "Current Balance",
            f"${current_balance:,.2f}",
            delta=f"${current_balance - (filtered_df[filtered_df['type'] == 'expense']['amount'].sum() if not filtered_df.empty else 0):,.2f}"
        )
    
    with col2:
        current_expenses = filtered_df[filtered_df['type'] == 'expense']['amount'].sum()
        last_expenses = df[pd.to_datetime(df['date']) < start_date][df['type'] == 'expense']['amount'].sum()
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
    
    # Recent Activity
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Recent Activity")
        if not filtered_df.empty:
            st.dataframe(
                filtered_df.tail(5),
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
        else:
            st.info("No recent activity in this time frame.")
    
    with col2:
        st.subheader("Quick Add")
        with st.form("quick_add", clear_on_submit=True):
            description = st.text_input("Description")
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
            col1, col2 = st.columns(2)
            with col1:
                op_type = st.selectbox("Type", ['expense', 'income'])
            with col2:
                category = st.selectbox("Category", 
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
                st.session_state.operations.append(new_operation)
                save_data()
                calculate_balance()
                st.success("Transaction added!")
                st.rerun()

# Operations
elif selected == "Operations":
    st.title("💼 Operations Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Upload csv", "All Operations", "Search", "Edit"])
        
    with tab1:
        st.subheader("Upload Operations CSV")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            # Read the CSV file
            df_upload = pd.read_csv(uploaded_file)
            
            # Validate the uploaded data
            required_columns = ['Date', 'Operation', 'Category', 'Amount Deducted', 'Gains', 'Balance', 'Month']
            if all(col in df_upload.columns for col in required_columns):
                for _, row in df_upload.iterrows():
                    # Parse the date and convert Amount Deducted and Gains to float
                    date_str = row['Date']
                    operation = row['Operation']
                    category = row['Category']
                    amount_deducted = float(row['Amount Deducted'])
                    gains = float(row['Gains'])
                    
                    # Determine the operation type based on Amount Deducted and Gains
                    if amount_deducted < 0:
                        op_type = 'expense'
                    elif gains > 0:
                        op_type = 'income'
                    else:
                        continue  # Skip rows that don't represent a transaction
                    
                    new_operation = {
                        'date': datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d'),
                        'description': operation,
                        'amount': abs(amount_deducted) if op_type == 'expense' else gains,  # Use absolute value for expenses
                        'type': op_type,
                        'category': category
                    }
                    st.session_state.operations.append(new_operation)
                save_data()
                calculate_balance()
                st.success("Operations added successfully!")
                st.experimental_rerun()
            else:
                st.error("Uploaded CSV must contain the following columns: " + ", ".join(required_columns))

    with tab2:
        if st.session_state.operations:
            df = pd.DataFrame(st.session_state.operations)
            df['date'] = pd.to_datetime(df['date'])
            
            # Filters
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
            
            # Apply filters
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
            df = pd.DataFrame(st.session_state.operations)
            results = df[df['description'].str.contains(search_term, case=False)]
            if not results.empty:
                st.dataframe(results, hide_index=True)
            else:
                st.info("No matching operations found.")
    
    with tab4:
        if st.session_state.operations:
            df = pd.DataFrame(st.session_state.operations)
            selected_index = st.selectbox(
                "Select operation to edit/delete",
                range(len(df)),
                format_func=lambda x: f"{df.iloc[x]['date']} - {df.iloc[x]['description']} (${df.iloc[x]['amount']:,.2f})"
            )
            
            if st.button("🗑️ Delete Operation", type="primary"):
                st.session_state.operations.pop(selected_index)
                save_data()
                calculate_balance()
                st.success("Operation deleted successfully!")
                st.rerun()

# Analytics
elif selected == "Analytics":
    st.title("📈 Financial Analytics")
    
    if st.session_state.operations:
        df = pd.DataFrame(st.session_state.operations)
        df['date'] = pd.to_datetime(df['date'])
        
        tab1, tab2, tab3 = st.tabs(["Category Analysis", "Time Analysis", "Trends"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Expenses by Category")
                expenses = df[df['type'] == 'expense']
                category_sum = expenses.groupby('category')['amount'].sum().reset_index()
                fig = px.pie(
                    category_sum,
                    values='amount',
                    names='category',
                    title='Expense Distribution'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Category Breakdown")
                st.dataframe(
                    category_sum,
                    column_config={
                        "category": "Category",
                        "amount": st.column_config.NumberColumn(
                            "Amount",
                            format="$%.2f"
                        )
                    },
                    hide_index=True
                )
        
        with tab2:
            st.subheader("Monthly Trends")
            df['month'] = df['date'].dt.strftime('%Y-%m')
            monthly_data = df.pivot_table(
                index='month',
                columns='type',
                values='amount',
                aggfunc='sum'
            ).fillna(0)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=monthly_data.index,
                y=monthly_data['expense'],
                name='Expenses',
                marker_color='red'
            ))
            fig.add_trace(go.Bar(
                x=monthly_data.index,
                y=monthly_data['income'],
                name='Income',
                marker_color='green'
            ))
            fig.update_layout(barmode='group', title='Monthly Income vs Expenses')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Balance Trend")
            df_sorted = df.sort_values('date')
            df_sorted['cumulative_balance'] = df_sorted.apply(
                lambda x: x['amount'] if x['type'] == 'income' else -x['amount'],
                axis=1
            ).cumsum()
            
            fig = px.line(
                df_sorted,
                x='date',
                y='cumulative_balance',
                title='Balance Over Time'
            )
            st.plotly_chart(fig, use_container_width=True)

# Reports
elif selected == "Reports":
    st.title("📑 Financial Reports")
    
    if st.session_state.operations:
        df = pd.DataFrame(st.session_state.operations)
        
        # Summary Statistics
        st.header("Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Income",
                f"${df[df['type'] == 'income']['amount'].sum():,.2f}"
            )
        with col2:
            st.metric(
                "Total Expenses",
                f"${df[df['type'] == 'expense']['amount'].sum():,.2f}"
            )
        with col3:
            st.metric(
                "Net Balance",
                f"${st.session_state.current_balance:,.2f}"
            )
        with col4:
            st.metric(
                "Transaction Count",
                len(df)
            )
        
        # Export Options
        st.header("Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV Report",
                data=csv,
                file_name="finance_report.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Excel export option (if xlsxwriter is installed)
            try:
                import xlsxwriter
                excel_buffer = pd.ExcelWriter('finance_report.xlsx', engine='xlsxwriter')
                df.to_excel(excel_buffer, index=False, sheet_name='Operations')
                excel_buffer.close()
                
                with open('finance_report.xlsx', 'rb') as f:
                    excel_data = f.read()
                
                st.download_button(
                    label="📥 Download Excel Report",
                    data=excel_data,
                    file_name="finance_report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except ImportError:
                st.info("Excel export requires xlsxwriter package. Install it using: pip install xlsxwriter")

# Settings
elif selected == "Settings":
    st.title("⚙️ Settings")
    
    st.header("Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Reset All Data", type="primary"):
            st.session_state.operations = []
            st.session_state.current_balance = 0.0
            save_data()
            # Reset the JSON file
            with open('operations.json', 'w') as f:
                json.dump([], f)  # Reset to empty list
            st.success("All data has been reset!")
            st.rerun()