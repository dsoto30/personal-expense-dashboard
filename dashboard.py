import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os


st.set_page_config(page_title="Personal Expense Dashboard", page_icon="./black-logo.png")

def parse_csv(file) -> any:
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
        
        return df
    except Exception as e:
        print(e)
        return None

def start_dashboard():
    st.title("Personal Finance Dashboard")

    statement = st.file_uploader("Please Upload Your Monthly Statements", type=['pdf', 'csv'])


    if statement is not None:
        df = parse_csv(statement)
        df 
if __name__ == "__main__":
    start_dashboard()