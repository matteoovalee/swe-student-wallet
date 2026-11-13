import streamlit as st
import pandas as pd
from smart.categorize import categorize

st.set_page_config(page_title="Student Wallet", page_icon="💳")

pages = ["Dashboard", "Transactions", "Exchange rate"]
selected_page = st.sidebar.radio("Navigate", pages)

st.title(selected_page)

if selected_page == "Dashboard":
    df = pd.read_csv("data/transactions.csv")
    df["month"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
    selected_month = st.selectbox("Select Month", sorted(df["month"].unique(), reverse=True))
    month_df = df[df["month"] == selected_month]

    expenses = month_df[(month_df["amount"] < 0) & (month_df["currency"] == "MYR")]
    expenses = expenses.copy()
    expenses["category"] = expenses["merchant"].apply(categorize)
    total_spending = -expenses["amount"].sum()
    st.metric("Total Monthly Spending", f"RM {total_spending:,.2f}")
    category_spending = expenses.groupby("category")["amount"].sum().abs()
    st.subheader("Spending by Category")
    st.bar_chart(category_spending)
    st.dataframe(category_spending.rename("Spending (RM)").reset_index())

    
elif selected_page == "Transactions":
    st.write("Transactions page")
else:
    st.write("Exchange rate page")
