import streamlit as st
import pandas as pd
from services.balance_calculator import BalanceCalculator

def render_reports(data_manager) -> None:
    st.title("📑 Financial Reports")
    currency_symbol = st.session_state.get("currency_symbol", "€")
    
    operations = data_manager.get_operations()
    if operations:
        df = pd.DataFrame(operations)
        
        st.header("Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Income",
                f"{df[df['type'] == 'income']['amount'].sum():,.2f}{currency_symbol}"
            )
        with col2:
            st.metric(
                "Total Expenses",
                f"{df[df['type'] == 'expense']['amount'].sum():,.2f}{currency_symbol}"
            )
        with col3:
            st.metric(
                "Net Balance",
                f"{BalanceCalculator.calculate_total_balance(operations):,.2f}{currency_symbol}"
            )
        with col4:
            st.metric(
                "Transaction Count",
                len(df)
            )
        
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
            try:
                buffer = pd.ExcelWriter('finance_report.xlsx', engine='xlsxwriter')
                df.to_excel(buffer, index=False, sheet_name='Operations')
                buffer.close()
                
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
    else:
        st.info("No data available for reporting. Add some transactions first!")
