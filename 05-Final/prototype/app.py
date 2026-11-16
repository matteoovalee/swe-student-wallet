from pathlib import Path

import pandas as pd
import streamlit as st

from smart.budget import budget_status, load_budget, parse_budget, save_budget
from smart.categorize import categorize
from smart.category_edit import CATEGORIES, change_categories, prepare


st.set_page_config(page_title="Student Wallet", page_icon="💳")

SAMPLE_CSV = Path(__file__).parent / "data" / "transactions.csv"
BUDGET_CSV = Path(__file__).parent / "data" / "budgets.csv"

if "transactions" not in st.session_state:
    st.session_state["transactions"] = None

# changes by 1 every time the student corrects a category, so the table starts fresh
if "edit_version" not in st.session_state:
    st.session_state["edit_version"] = 0

pages = ["Dashboard", "Transactions", "Exchange rate"]
selected_page = st.sidebar.radio("Navigate", pages)

st.title(selected_page)

if selected_page == "Dashboard":
    if st.session_state["transactions"] is None:
        st.info(
            "Showing the sample data. Import your own CSV file on the "
            "Transactions page to see your spending."
        )
        if "sample_transactions" not in st.session_state:
            st.session_state["sample_transactions"] = prepare(
                pd.read_csv(SAMPLE_CSV, encoding="utf-8-sig")
            )
        data_key = "sample_transactions"
    else:
        data_key = "transactions"

    df = prepare(st.session_state[data_key])
    df["month"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
    selected_month = st.selectbox("Select Month", sorted(df["month"].unique(), reverse=True))
    month_df = df[df["month"] == selected_month]

    expenses = month_df[(month_df["amount"] < 0) & (month_df["currency"] == "MYR")]
    total_spending = -expenses["amount"].sum() + 0.0  # + 0.0: no "-0.00" when there is no spending
    st.metric("Total Monthly Spending", f"RM {total_spending:,.2f}")

    st.subheader("Monthly Budget")
    saved_budget = load_budget(BUDGET_CSV, selected_month)
    budget_text = st.text_input(
        "Budget for this month (RM)",
        value="" if saved_budget is None else f"{saved_budget:.2f}",
        key=f"budget_{selected_month}",
    )
    if st.button("Save budget"):
        try:
            new_budget = parse_budget(budget_text)
        except ValueError as error:
            st.error(str(error))
        else:
            save_budget(BUDGET_CSV, selected_month, new_budget)
            saved_budget = new_budget
            st.success("Budget saved.")

    if saved_budget is None:
        st.info("No budget set for this month.")
    else:
        used, left = budget_status(saved_budget, total_spending)
        budget_col, used_col, left_col = st.columns(3)
        budget_col.metric("Budget", f"RM {saved_budget:,.2f}")
        used_col.metric("Used", f"RM {used:,.2f}")
        if left < 0:
            left_col.markdown(f"Left\n\n## :red[RM {left:,.2f}]")
        else:
            left_col.metric("Left", f"RM {left:,.2f}")

    if expenses.empty:
        st.info("No MYR expenses in this month.")
    else:
        category_spending = expenses.groupby("category")["amount"].sum().abs()
        st.subheader("Spending by Category")
        st.bar_chart(category_spending)
        st.dataframe(category_spending.rename("Spending (RM)").reset_index())

    st.subheader("Transactions of the Month")
    st.caption("Wrong category? Change it in the table. The chart and the totals update.")
    columns = ["date", "merchant", "amount", "currency", "category", "category_source"]
    shown = month_df[columns]
    edited = st.data_editor(
        shown,
        hide_index=True,
        disabled=[column for column in columns if column != "category"],
        column_config={
            "category": st.column_config.SelectboxColumn(
                "Category", options=CATEGORIES, required=True
            )
        },
        key=f"editor_{selected_month}_{st.session_state['edit_version']}",
    )
    if not edited["category"].equals(shown["category"]):
        st.session_state[data_key] = change_categories(df.drop(columns="month"), edited)
        st.session_state["edit_version"] += 1
        st.rerun()

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
                    preview["category_source"] = "auto"

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