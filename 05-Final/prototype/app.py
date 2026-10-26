import streamlit as st

st.set_page_config(page_title="Student Wallet", page_icon="💳")

pages = ["Dashboard", "Transactions", "Exchange rate"]
selected_page = st.sidebar.radio("Navigate", pages)

st.title(selected_page)

if selected_page == "Dashboard":
    st.write("Dashboard page")
elif selected_page == "Transactions":
    st.write("Transactions page")
else:
    st.write("Exchange rate page")
