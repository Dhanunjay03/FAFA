import streamlit as st
import pandas as pd
import numpy as np

title=st.container()
with title:
    st.title("Financial Assistance for Analysis")
    # st.header("Hello Pujitha")

st.write("---")

# File
df=pd.read_excel("data.xlsx")

# Type conversion of int64 to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Total Data Description
output1=st.container()
with output1:
    st.header("statistical Output")
    st.write("Here is the statistical data of Entire Data...")
    Total_Revenue=np.sum(df["Amount"])
    Total_collected=np.sum(df[df["Status"]=="Paid"]["Amount"])
    To_be_collected=Total_Revenue-Total_collected
    st.text(f"* Total Revenue Generated : Rs.{Total_Revenue}.00")
    st.text(f"* Total Revenue Collected : Rs.{Total_collected}.00")
    st.text(f"* Revenue To be Collected : Rs.{To_be_collected}.00")
    # st.write("***")
    # st.header("Description")
    # st.write(df.describe())
    # st.dataframe(df,width=700,height=1070)

# SideBar
sidebar=st.container()
with sidebar:
    st.sidebar.subheader("Select Region:")
    city=st.sidebar.multiselect("Select The area:",df["Address"].unique())    

    st.sidebar.subheader("Select Date Range:")
    start_date = pd.to_datetime(st.sidebar.date_input("Start Date", df['Date'].min()))
    end_date = pd.to_datetime(st.sidebar.date_input("End Date", df['Date'].max()))
    
    st.sidebar.subheader("Select Order")
    item=st.sidebar.selectbox("Select the product:",df["Order"].unique())
st.write("---")
# Sum of City
sum=st.container()
with sum or (start_date and end_date) or item:
    # if city:
    #     st.subheader("Statistics about selected Address")
    #     # filtered_df = df[df["Address"].isin(city)]
    #     filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date) & (df['Address'].isin(city))]
    #     sum_of_area=np.sum(filtered_df["Amount"])
    #     collected_amount=np.sum(filtered_df[filtered_df["Status"]=="Paid"]["Amount"])
    #     pending_amount=np.sum(filtered_df[filtered_df["Status"]=="Pending"]["Amount"])
       
    #     if(sum_of_area==collected_amount+pending_amount):
    #         st.markdown(f"* Total Amount from {city}: Rs.{sum_of_area}.00")
    #         st.markdown(f"* Total Amount Collected from {city}: Rs.{collected_amount}.00")
    #         st.markdown(f"* Total Amount To be Collected from {city}: Rs.{pending_amount}.00")
    #     else:
    #         # Trigger Error Message When Amount is missing or incorrect! 
    #         st.text("Something Went wrong!\nPlease chek your data!!!!")
    if city or (start_date and end_date) or item:
        st.subheader("Statistics based on selected criteria")
        # Filter DataFrame based on city, date range, and order
        filtered_df = df[
            (df['Date'] >= start_date) & (df['Date'] <= end_date) &
            (df['Address'].isin(city)) & (df['Order'] == item)
        ]

        sum_of_area = np.sum(filtered_df["Amount"])
        collected_amount = np.sum(filtered_df[filtered_df["Status"] == "Paid"]["Amount"])
        pending_amount = np.sum(filtered_df[filtered_df["Status"] == "Pending"]["Amount"])

        if sum_of_area == collected_amount + pending_amount:
            st.markdown(f"* Total Amount from {city} with Order {item}: Rs.{sum_of_area}.00")
            st.markdown(f"* Total Amount Collected from {city} with Order {item}: Rs.{collected_amount}.00")
            st.markdown(f"* Total Amount To be Collected from {city} with Order {item}: Rs.{pending_amount}.00")
        else:
            # Trigger Error Message When Amount is missing or incorrect!
            st.text("Something Went wrong!\nPlease check your data!!!!")
    else:
        st.text("Please select one or more cities, specify a date range, or enter an order.")
        
    