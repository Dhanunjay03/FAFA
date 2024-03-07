import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load data with caching
# buttons="""<button class="btn btn-danger">Home</button>"""
# name="""<body><h1 id="h1" style="background-color:green;"></h1>
#       <marquee direction="right">sravan</marquee>
#       <script>
#          document.getElementById("h1").innerHTML="sravan potnuru"
#       </script></body>"""
#st.markdown(name,unsafe_allow_html=True)
#st.markdown(buttons,unsafe_allow_html=True)
@st.cache_data
def load_data():    
    df = pd.read_excel("data.xlsx")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Function to display statistics
def display_statistics(filtered_df, city, start_date, end_date, item):
    st.subheader("Statistics based on selected criteria")
    
    if city:
        st.markdown(f"* Selected Area(s): {', '.join(city)}")

    if start_date and end_date:
        st.markdown(f"* Selected Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    if item:
        st.markdown(f"* Selected Product: {item}")

    if not filtered_df.empty:
        sum_of_area = np.sum(filtered_df["Amount"])
        collected_amount = np.sum(filtered_df[filtered_df["Status"] == "Paid"]["Amount"])
        pending_amount = np.sum(filtered_df[filtered_df["Status"] == "Pending"]["Amount"])

        # Display Order information only if it's not None
        order_info = f" with Order {item}" if item is not None else ""

        if city:
            area_info = f" from {', '.join(city)}"
        else:
            area_info = ""

        if sum_of_area == collected_amount + pending_amount:
            st.markdown(f"* Total Amount{area_info}{order_info}: Rs.{sum_of_area:.2f}")
            st.markdown(f"* Total Amount Collected{area_info}{order_info}: Rs.{collected_amount:.2f}")
            st.markdown(f"* Total Amount To be Collected{area_info}{order_info}: Rs.{pending_amount:.2f}")
            display_order_pie_chart(filtered_df, item)
        else:
            st.text("Something Went wrong!\nPlease check your data!!!!")
    else:
        st.text("No data matching the selected criteria.")

def display_order_pie_chart(filtered_df, order):
    if order:
        # Filter data for the selected order
        order_df = filtered_df[filtered_df['Order'] == order]

        # Create a pie chart based on the amount of the selected order sold in each area
        fig_pie = px.pie(
            order_df,
            names='Address',
            values='Amount',
            title=f'Amount Distribution of Order {order} in All Areas',
            hole=0.3,
            labels={'Amount': 'Amount Sold'}
        )
        st.plotly_chart(fig_pie)

# Main Streamlit App
title = st.container()
with title:
    st.title("Financial Assistance for Analysis")

st.write("---")

# **File Upload Container**
file_upload_container = st.container()
with file_upload_container:
    uploaded_file = st.file_uploader("Upload your data file (Excel format)", type="xlsx")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        # Get user input for column name mappings (default to some common attributes)
        col_map = {
            "Location": st.sidebar.text_input("Enter the name of the location attribute:", "Address"),
            "Date": st.sidebar.text_input("Enter the name of the date attribute:", "Date"),
            "Amount": st.sidebar.text_input("Enter the name of the amount attribute:", "Amount"),
            "Status": st.sidebar.text_input("Enter the name of the status attribute:", "Status"),
            "Order": st.sidebar.text_input("Enter the name of the order attribute:", "Order (optional)"),
        }

        # Check for missing user-defined columns and update the DataFrame if needed
        missing_cols = [col for col, user_col in col_map.items() if user_col not in df.columns]
        if missing_cols:
            st.error(f"Error: The following attributes are missing in the uploaded data: {', '.join(missing_cols)}")
            df = pd.DataFrame()  # Create an empty DataFrame in case of errors
        else:
            # Assuming all user-defined columns exist, update DataFrame column names
            df.rename(columns=col_map, inplace=True)

            # Convert date column to datetime format (assuming it exists)
            if "Date" in col_map.values():
                df[col_map["Date"]] = pd.to_datetime(df[col_map["Date"]])
            # Hide the file upload container after successful verification
            file_upload_container.empty()
        # Sidebar Container (assuming data is loaded)
        if not df.empty:
            # Statistical Output Container
            output1 = st.container()
            with output1:
                #st.write(df.head())
                st.header("Statistical Output")
                st.write("Here is the statistical data of the Entire Data...")
                Total_Revenue = np.sum(df["Amount"])
                Total_collected = np.sum(df[df["Status"] == "Paid"]["Amount"])
                To_be_collected = Total_Revenue - Total_collected
                st.text(f"* Total Revenue Generated: Rs.{Total_Revenue:.2f}")
                st.text(f"* Total Revenue Collected: Rs.{Total_collected:.2f}")
                st.text(f"* Revenue To be Collected: Rs.{To_be_collected:.2f}")

            # Sidebar Container
            sidebar = st.sidebar.container()
            with sidebar:
                st.image("/home/dhanunjay/Desktop/myproject/icons/FaFa_icon_rmbg.png",width=200)
                st.sidebar.subheader("Select Region:")
                city = st.sidebar.multiselect("Select The area:", df["Address"].unique(),default=None)

                st.sidebar.subheader("Select Date Range:")
                start_date = pd.to_datetime(st.sidebar.date_input("Start Date", df['Date'].min()))
                end_date = pd.to_datetime(st.sidebar.date_input("End Date", "today"))
                

                # Optional Order Selection
                # if st.sidebar.checkbox("Filter by Order"):
                # item = None
                
                item = st.sidebar.selectbox("Select the product:", df["Order"].unique(),index=None)
                    
            st.write("---")

            # Statistics Container
            if item or city:
                statistics_container = st.container()
                with statistics_container:
                    # st.subheader("Statistics based on selected criteria")

                    # Check if any filter is applied
                    if city and (start_date is not None) and (end_date is not None) and (item is not None):
                        # All filters are selected
                        filtered_df = df[
                            (df['Date'] >= start_date) & (df['Date'] <= end_date) &
                            (df['Address'].isin(city)) & (df['Order'] == item)
                        ]
                        display_statistics(filtered_df, city, start_date, end_date, item)

                    elif city and (start_date is not None) and (end_date is not None):
                        # Only city, start_date, and end_date are selected
                        filtered_df = df[
                            (df['Date'] >= start_date) & (df['Date'] <= end_date) & (df['Address'].isin(city))
                        ]
                        display_statistics(filtered_df, city, start_date, end_date, item)

                    elif city and (item is not None):
                        # Only city and item are selected
                        filtered_df = df[
                            (df['Address'].isin(city)) & (df['Order'] == item)
                        ]
                        display_statistics(filtered_df, city, start_date, end_date, item)

                    elif (start_date is not None) and (end_date is not None) and (item is not None):
                        # Only start_date, end_date, and item are selected
                        filtered_df = df[
                            (df['Date'] >= start_date) & (df['Date'] <= end_date) & (df['Order'] == item)
                        ]
                        display_statistics(filtered_df, city, start_date, end_date, item)

                    elif city:
                        # Only city is selected
                        filtered_df = df[
                            (df['Date'] >= start_date) & (df['Date'] <= end_date) & (df['Address'].isin(city))
                        ]
                        display_statistics(filtered_df, city, start_date, end_date, item)

                    elif (start_date is not None) and (end_date is not None):
                        # Only start_date and end_date are selected
                        filtered_df = df[
                            (df['Date'] >= start_date) & (df['Date'] <= end_date)
                        ]
                        display_statistics(filtered_df, city, start_date, end_date, item)

                    elif item:
                        # Only item is selected
                        filtered_df = df[
                            (df['Order'] == item)
                        ]
                        display_statistics(filtered_df, city, start_date, end_date, item)

                    else:
                        st.text("Please select one or more filters.")
                    
                # Graphs
                
                # Pie chart for 'Amount' based on 'Payment_Status'
                    
                total_order_quantity = np.sum(filtered_df["Quantity"])
                fig = px.pie(
                    filtered_df,
                    names='Status',
                    values='Amount',
                    title=f'Amount Breakdown for {", ".join(city)}',
                    hole=0.3,
                    labels={"Amount":"Total Amount"}
                )
                st.plotly_chart(fig)

                # Bar chart for total order quantity per locality
                fig_bar = px.bar(
                    filtered_df,
                    x='Address',
                    y='Quantity',
                    title=f'Total Order Quantity for each Locality ({", ".join(city)})',
                    labels={'Quantity': 'Total Order Quantity'},
                    color='Address',
                    height=400
                )
                st.plotly_chart(fig_bar)
                
                # Line chart for order quantities over time
                
                fig_line = px.line(
                    filtered_df,
                    x='Date',
                    y='Quantity',
                    title='Order Quantities Over Time',
                    labels={'Quantity': 'Order Quantity'},
                    markers=True
                )
                st.plotly_chart(fig_line)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        df = pd.DataFrame()  # Create an empty DataFrame in case of errors



# # Load Data
# df = load_data()

