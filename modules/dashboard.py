import streamlit as st
from components.quick_add_form import render_quick_add_form
from components.metrics_display import render_key_metrics
from datetime import datetime, timedelta

def render_dashboard(data_manager) -> None:
    st.title("📊 Financial Dashboard")
    
    # Time Frame Selector
    time_frame = st.selectbox(
        "Select Time Frame",
        ["Week", "Month", "Year"]
    )
    
    # Render Key Metrics
    render_key_metrics(data_manager, time_frame)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Recent Activity")
        
        # Fetch and filter operations
        operations = data_manager.get_operations()
        if operations:
            import pandas as pd
            
            # Convert operations into a DataFrame
            df = pd.DataFrame(operations)
            
            # Ensure 'date' column is in datetime format
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            
            # Calculate date range for the selected time frame
            now = datetime.now()
            if time_frame == "Week":
                start_date = now - timedelta(weeks=1)
                end_date = now
            elif time_frame == "Month":
                start_date = now - timedelta(days=30)
                end_date = now
            else:  # Year
                start_date = now - timedelta(days=365)
                end_date = now
            
            # Filter operations by the time frame
            filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
            
            # Reverse order of operations (latest first)
            filtered_df = filtered_df.sort_values(by="date", ascending=False)
            
            # Display the filtered DataFrame
            if not filtered_df.empty:
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
            else:
                st.info(f"No recent activity for the selected period ({time_frame.lower()}).")
        else:
            st.info("No recent activity.")
    
    with col2:
        st.subheader("Quick Add")
        render_quick_add_form(data_manager)
