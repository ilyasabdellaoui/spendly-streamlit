import streamlit as st
from components.quick_add_form import render_quick_add_form
from components.metrics_display import render_key_metrics
from datetime import datetime, timedelta

def render_dashboard(data_manager) -> None:
    st.title("📊 Financial Dashboard")
    
    # Time Frame Selector
    time_frame = st.selectbox(
        "Select Time Frame",
        ["Week", "Month", "Quarter", "Year", "Custom"]
    )
    
    # Get date range based on selection
    end_date = datetime.now()
    
    if time_frame == "Custom":
        date_range = st.date_input(
            "Select date range",
            value=(end_date - timedelta(days=7), end_date),
            max_value=end_date
        )
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date = end_date - timedelta(days=7)
    else:
        if time_frame == "Week":
            start_date = end_date - timedelta(days=7)
        elif time_frame == "Month":
            start_date = end_date - timedelta(days=30)
        elif time_frame == "Quarter":
            start_date = end_date - timedelta(days=90)
        else:  # Last year
            start_date = end_date - timedelta(days=365)
    
    # Render Key Metrics with guaranteed non-None dates
    render_key_metrics(data_manager, start_date, end_date)
    
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
            
            # Filter operations by the selected date range
            filtered_df = df[(df["date"] >= pd.to_datetime(start_date)) & 
                           (df["date"] <= pd.to_datetime(end_date))]
            
            # Reverse order of operations (latest first)
            filtered_df = filtered_df.sort_values(by="date", ascending=False)
            
            # Display the filtered DataFrame
            if not filtered_df.empty:
                st.dataframe(
                    filtered_df,
                    column_config={
                        "date": st.column_config.DatetimeColumn(
                            "Date",
                            format="MMM DD, YYYY"
                        ),
                        "description": "Description",
                        "amount": st.column_config.NumberColumn(
                            "Amount",
                            format="$%.2f"
                        ),
                        "type": st.column_config.Column(
                            "Type",
                            width="small"
                        ),
                        "category": st.column_config.Column(
                            "Category",
                            width="small"
                        )
                    },
                    hide_index=True
                )
                
                st.caption(f"Showing transactions from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")
            else:
                st.info(f"No activity found between {start_date.strftime('%B %d, %Y')} and {end_date.strftime('%B %d, %Y')}")
        else:
            st.info("No recent activity.")
    
    with col2:
        st.subheader("Quick Add")
        render_quick_add_form(data_manager)