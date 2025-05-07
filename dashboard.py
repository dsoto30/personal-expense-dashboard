import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os


st.set_page_config(page_title="Personal Expense Dashboard", page_icon="./black-logo.png")

def start_dashboard():
    st.title("Personal Finance Dashboard")

    statement = st.file_uploader("Please Upload Your Monthly Statements", type=['pdf', 'csv'])


    if statement is not None:
        print("Statement")
if __name__ == "__main__":
    start_dashboard()