import streamlit as st
from components.quick_add_form import render_quick_add_form
from components.metrics_display import render_key_metrics

def render_dashboard(data_manager) -> None:
    st.title("📊 Financial Dashboard")
    
    time_frame = st.selectbox(
        "Select Time Frame",
        ["Week", "Month", "Year", "All Time"]
    )
    
    render_key_metrics(data_manager, time_frame)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Recent Activity")
        operations = data_manager.get_operations()
        if operations:
            import pandas as pd
            df = pd.DataFrame(operations)
            st.dataframe(
                df.tail(5),
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
            st.info("No recent activity.")
    
    with col2:
        st.subheader("Quick Add")
        render_quick_add_form(data_manager)