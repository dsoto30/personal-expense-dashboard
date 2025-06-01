import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os


st.set_page_config(page_title="Personal Expense Dashboard", page_icon="./black-logo.png")

def parse_wells_fargo(file) -> any:
    try:
        df = pd.read_csv(file, header=None, names=["Date", "Amount", "Status", "Check_Number", "Description"], dtype=str)
        df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce").dt.date
        df["Amount"] = (
            df["Amount"]
            .str.replace(r"[\$,]", "", regex=True)
            .astype(float)
        )
        
        # 4. Label each transaction as 'expense' or 'surplus'
        df["Type"] = df["Amount"].apply(lambda x: "expense" if x < 0 else "surplus")
        
        # Drop unnecessary columns
        df = df.drop(columns=["Status", "Check_Number"])
        
        return df
    except Exception as e:
        print(f"Error parsing Wells Fargo CSV: {e}")
        return None
    
def parse_discover_csv(file) -> any:
    try:
        df = pd.read_csv(file, dtype=str)
        df = df.drop(columns=["Post Date", "Category"])
        df = df.rename(columns={"Trans. Date": "Date"})
        df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce").dt.date
        df["Amount"] = (
            df["Amount"]
            .str.replace(r"[\$,]", "", regex=True)
            .astype(float)
        )
        
        # 4. Label each transaction as 'expense' or 'surplus'
        df["Type"] = df["Amount"].apply(lambda x: "expense" if x > 0 else "surplus")

        return df 
    except Exception as e:
        print(f"Error reading Discover CSV: {e}")
        return None

def start_dashboard():
    st.title("Personal Finance Dashboard")
    # Bank selection dropdown
    bank = st.selectbox("Select Your Bank", ["Wells Fargo", "Discover"])

    statement = st.file_uploader("Please Upload Your Monthly Statements", type=['csv'])

    if bank == "Wells Fargo" and statement is not None:
        df = parse_wells_fargo(statement)
        if df is not None:
            st.write("### Transaction Data")
            st.dataframe(df)

            # Display total expenses and surplus
            total_expenses = df[df["Type"] == "expense"]["Amount"].sum()
            total_surplus = df[df["Type"] == "surplus"]["Amount"].sum()

            st.write(f"**Total Expenses:** ${total_expenses:.2f}")
            st.write(f"**Total Surplus:** ${total_surplus:.2f}")

            # Plotting the data
            fig = px.bar(df, x="Date", y="Amount", color="Type", title="Monthly Transactions")
            st.plotly_chart(fig)

    elif bank == "Discover" and statement is not None:
        df = parse_discover_csv(statement)
        if df is not None:
            st.write("### Transaction Data")
            st.dataframe(df)

            # Display total expenses and surplus
            total_expenses = df[df["Type"] == "expense"]["Amount"].sum()
            total_surplus = df[df["Type"] == "surplus"]["Amount"].sum()

            st.write(f"**Total Expenses:** ${total_expenses:.2f}")
            st.write(f"**Total Surplus:** ${total_surplus:.2f}")

            # Plotting the data
            fig = px.bar(df, x="Date", y="Amount", color="Type", title="Monthly Transactions")
            st.plotly_chart(fig)

if __name__ == "__main__":
    start_dashboard()
# This code is a Streamlit application that serves as a personal finance dashboard.
# It allows users to upload their monthly bank statements and visualize their expenses and surplus.
# The application currently supports Wells Fargo CSV statements and has a placeholder for Discover CSV parsing.