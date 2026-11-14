from pathlib import Path

import pandas as pd
import streamlit as st

from smart.categorize import categorize


st.set_page_config(page_title="Student Wallet", page_icon="💳")

SAMPLE_CSV = Path(__file__).parent / "data" / "transactions.csv"

if "transactions" not in st.session_state:
    st.session_state["transactions"] = None

pages = ["Dashboard", "Transactions", "Exchange rate"]
selected_page = st.sidebar.radio("Navigate", pages)

st.title(selected_page)

if selected_page == "Dashboard":
    transactions = st.session_state["transactions"]

    if transactions is None:
        st.info(
            "Showing the sample data. Import your own CSV file on the "
            "Transactions page to see your spending."
        )
        df = pd.read_csv(SAMPLE_CSV, encoding="utf-8-sig")
    else:
        df = transactions.copy()

    if "category" not in df.columns:
        df["category"] = df["merchant"].apply(categorize)
    df["month"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
    selected_month = st.selectbox("Select Month", sorted(df["month"].unique(), reverse=True))
    month_df = df[df["month"] == selected_month]

    expenses = month_df[(month_df["amount"] < 0) & (month_df["currency"] == "MYR")]
    total_spending = -expenses["amount"].sum()
    st.metric("Total Monthly Spending", f"RM {total_spending:,.2f}")

    if expenses.empty:
        st.info("No MYR expenses in this month.")
    else:
        category_spending = expenses.groupby("category")["amount"].sum().abs()
        st.subheader("Spending by Category")
        st.bar_chart(category_spending)
        st.dataframe(category_spending.rename("Spending (RM)").reset_index())

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
                valid_dates = pd.to_datetime(preview["date"], errors="coerce")
                valid_amounts = pd.to_numeric(preview["amount"], errors="coerce")
                bad_rows = preview[valid_dates.isna() | valid_amounts.isna()]

                if not bad_rows.empty:
                    # +2: the header is line 1 and the index starts at 0
                    lines = ", ".join(str(i + 2) for i in bad_rows.index[:5])
                    st.error(
                        f"{len(bad_rows)} row(s) have an invalid date or amount "
                        f"(CSV line {lines}). Nothing was imported."
                    )
                else:
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