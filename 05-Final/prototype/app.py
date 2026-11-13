import pandas as pd
import streamlit as st

from smart.categorize import categorize


st.set_page_config(page_title="Student Wallet", page_icon="💳")

if "transactions" not in st.session_state:
    st.session_state["transactions"] = None

pages = ["Dashboard", "Transactions", "Exchange rate"]
selected_page = st.sidebar.radio("Navigate", pages)

st.title(selected_page)

if selected_page == "Dashboard":
    transactions = st.session_state["transactions"]

    if transactions is None:
        st.info("Import a CSV file from the Transactions page to get started.")
    else:
        st.write(f"Imported transactions: {len(transactions)}")
        st.dataframe(transactions, hide_index=True)

elif selected_page == "Transactions":
    uploaded_file = st.file_uploader("Upload a transactions CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            uploaded_data = pd.read_csv(uploaded_file, encoding="utf-8-sig")
            required_columns = ["date", "merchant", "amount", "currency"]
            missing_columns = [
                column for column in required_columns
                if column not in uploaded_data.columns
            ]

            if missing_columns:
                st.error(
                    "Missing required columns: "
                    + ", ".join(missing_columns)
                    + ". Nothing was imported."
                )
            else:
                preview = uploaded_data[required_columns].copy()
                preview["category"] = preview["merchant"].apply(categorize)

                st.subheader("Preview")
                st.dataframe(preview, hide_index=True)

                if st.button("Confirm import"):
                    st.session_state["transactions"] = preview
                    st.success(
                        f"Imported {len(preview)} transactions. "
                        "They are now available on the Dashboard."
                    )

        except Exception as error:
            st.error(f"Could not read the CSV file: {error}")

else:
    st.write("Exchange rate page")
