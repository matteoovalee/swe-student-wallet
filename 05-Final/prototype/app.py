from calendar import monthrange
from datetime import date, datetime, timedelta
import json
from math import isfinite
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import altair as alt
import pandas as pd
import streamlit as st

from smart.budget import budget_status, load_budget, parse_budget, save_budget
from smart.categorize import categorize
from smart.category_edit import CATEGORIES, change_categories, prepare


st.set_page_config(page_title="Student Wallet", page_icon="💳", layout="wide")

SAMPLE_CSV = Path(__file__).parent / "data" / "transactions.csv"
BUDGET_CSV = Path(__file__).parent / "data" / "budgets.csv"

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, .stApp, [data-testid="stSidebar"] { font-family: 'Inter', system-ui, sans-serif; }
[data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer { display: none !important; }
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1500px; }
h1 { font-size: 1.75rem !important; font-weight: 650 !important; letter-spacing: -0.01em; }
h3 { font-size: 1.05rem !important; font-weight: 600 !important; }
[class*="st-key-card"], [class*="st-key-kpi"] {
    background: #FFFFFF;
    border: 1px solid #E6EBEF !important;
    border-radius: 16px;
    padding: 0.5rem 0.75rem;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 6px 16px rgba(15, 23, 42, 0.04);
}
[data-testid="stMetricLabel"] p { color: #64748B; font-size: 0.85rem; font-weight: 500; }
[data-testid="stMetricValue"] { font-size: 1.9rem; font-weight: 650; }
[data-testid="stAlert"] { border-radius: 12px; }
.stButton > button { border-radius: 10px; font-weight: 500; }
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)


def save_budget_from_form(month):
    """Runs when Save budget is clicked, before the page is drawn again."""
    try:
        amount = parse_budget(st.session_state[f"budget_{month}"])
    except ValueError as error:
        st.session_state["budget_feedback"] = ("error", str(error))
    else:
        save_budget(BUDGET_CSV, month, amount)
        st.session_state["budget_feedback"] = ("success", "Budget saved.")


@st.cache_data(ttl=3600, show_spinner=False)
def daily_transfer_rates(currency, end):
    """Return available MYR-per-home-currency quotes in the last 30 calendar days."""
    start = end - timedelta(days=29)
    query = urlencode({"base": currency, "quotes": "MYR",
                       "from": start.isoformat(), "to": end.isoformat()})
    with urlopen(f"https://api.frankfurter.dev/v2/rates?{query}", timeout=8) as response:
        rows = json.load(response)
    daily = {}
    for row in rows:
        day = date.fromisoformat(row["date"])
        rate = float(row["rate"])
        if (row["base"] == currency and row["quote"] == "MYR"
                and start <= day <= end and isfinite(rate) and rate > 0):
            daily[day] = rate
    return daily


def show_forecast(transactions, as_of, currency, quote):
    from smart.forecast import forecast_end_of_month

    dates = pd.to_datetime(transactions["date"]).dt.date
    amounts = pd.to_numeric(transactions["amount"])
    recorded = (transactions["currency"] == "MYR") & (dates <= as_of)
    month_amounts = amounts[recorded & (dates >= as_of.replace(day=1))]
    if month_amounts.empty:
        st.info("No MYR transactions recorded for this month through the selected date.")
        return

    balance = amounts[recorded].sum()
    spent = -month_amounts[month_amounts < 0].sum() + 0.0
    days = monthrange(as_of.year, as_of.month)[1]
    forecast = forecast_end_of_month(balance, spent, as_of.day, days)
    left, right = st.columns([3, 2])
    with left.container(border=True, key="card_forecast"):
        st.subheader("Balance forecast")
        st.metric(f"Estimated balance on {as_of.replace(day=days):%d %b}", f"RM {forecast:,.2f}")
        if quote is not None:
            st.metric(f"Estimate in {currency}", f"{currency} {forecast * quote:,.2f}")
        else:
            st.caption(f"Conversion to {currency} is unavailable.")
        if as_of.day < days:
            dates_left = pd.date_range(as_of, periods=days - as_of.day + 1)
            projection = pd.Series(
                [balance - spent / as_of.day * i for i in range(len(dates_left))],
                index=dates_left, name="Balance (MYR)",
            )
            st.line_chart(projection, height=190)
    with right.container(border=True, key="card_spending"):
        st.subheader("Spending prediction")
        st.metric("Recorded balance", f"RM {balance:,.2f}")
        st.write(f"Spent this month: RM {spent:,.2f}")
        st.write(f"Expected spending through month end: RM {balance - forecast:,.2f}")
        st.caption("Uses all recorded MYR transactions for the balance and this month's "
                   "average daily spending. Future deposits are excluded.")


def show_rate_alert(currency, quote, today):
    from smart.alerts import alert_triggered, default_target

    history_key = f"transfer_history_{currency}"
    try:
        daily = daily_transfer_rates(currency, today)
        if not daily:
            raise ValueError("No daily rates returned")
        st.session_state[history_key] = daily
        history_source = "Published daily rates"
    except (URLError, OSError, ValueError, KeyError, TypeError):
        cutoff = today - timedelta(days=29)
        daily = {day: rate for day, rate in st.session_state.get(history_key, {}).items()
                 if cutoff <= day <= today}
        history_source = "Saved daily rates"

    average = default_target([daily[d] for d in sorted(daily)]) if daily else None
    alert_col, settings_col = st.columns([3, 2])
    targets = st.session_state.setdefault("transfer_targets", {})
    with settings_col.container(border=True, key="card_alert_settings"):
        st.subheader("Alert settings")
        if average is not None:
            st.write(f"30-day average: {average:.4f} MYR per {currency}")
            st.caption(f"{history_source} · {len(daily)} quoted days")
        else:
            st.caption("30-day average unavailable. Enter a target to check the rate.")
        with st.form(f"target_form_{currency}"):
            target_input = st.number_input(
                f"Target (MYR per {currency})", value=targets.get(currency),
                min_value=0.000001, format="%.6f", step=0.01,
                placeholder="Use the 30-day average",
            )
            if st.form_submit_button("Save target"):
                targets[currency] = target_input

    with alert_col.container(border=True, key="card_rate_alert"):
        st.subheader("Exchange rate alert")
        target = targets.get(currency)
        if target is None:
            target = average
        if quote is None:
            st.info(f"No current {currency} rate available.")
            return
        transfer_rate = 1 / quote
        st.metric("Current transfer rate", f"1 {currency} = {transfer_rate:.4f} MYR")
        if target is None:
            st.info("Waiting for a target or the 30-day average.")
        elif alert_triggered(transfer_rate, target):
            relation = "at" if transfer_rate == target else "above"
            st.success(f"Good time to transfer: 1 {currency} = {transfer_rate:.4f} MYR, "
                       f"{relation} your target of {target:.4f}.")
        else:
            st.info(f"Below your target of {target:.4f} MYR per {currency}.")
        st.caption(f"Checked {datetime.now().astimezone():%d %b %Y, %H:%M %Z}")


if "transactions" not in st.session_state:
    st.session_state["transactions"] = None

# changes by 1 every time the student corrects a category, so the table starts fresh
if "edit_version" not in st.session_state:
    st.session_state["edit_version"] = 0

pages = ["Dashboard", "Transactions", "Forecast and alerts"]
page_icons = {
    "Dashboard": ":material/dashboard:",
    "Transactions": ":material/upload_file:",
    "Forecast and alerts": ":material/currency_exchange:",
}
st.sidebar.markdown("### :material/account_balance_wallet: Student Wallet")
selected_page = st.sidebar.radio(
    "Navigate", pages, format_func=lambda page: f"{page_icons[page]} {page}"
)

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
    month_col, _ = st.columns([1, 3])
    selected_month = month_col.selectbox(
        "Select Month", sorted(df["month"].unique(), reverse=True)
    )
    month_df = df[df["month"] == selected_month]

    expenses = month_df[(month_df["amount"] < 0) & (month_df["currency"] == "MYR")]
    total_spending = -expenses["amount"].sum() + 0.0  # + 0.0: no "-0.00" when there is no spending
    saved_budget = load_budget(BUDGET_CSV, selected_month)

    if saved_budget is None:
        with st.container(border=True, key="kpi_spent"):
            st.metric("Total Monthly Spending", f"RM {total_spending:,.2f}")
    else:
        used, left = budget_status(saved_budget, total_spending)
        budget_col, used_col, left_col = st.columns(3)
        with budget_col.container(border=True, key="kpi_budget"):
            st.metric("Budget", f"RM {saved_budget:,.2f}")
        with used_col.container(border=True, key="kpi_used"):
            st.metric("Used", f"RM {used:,.2f}")
        with left_col.container(border=True, key="kpi_left"):
            if left < 0:
                st.markdown(f"Left\n\n## :red[RM {left:,.2f}]")
            else:
                st.metric("Left", f"RM {left:,.2f}")

    chart_col, side_col = st.columns([3, 2])

    with side_col:
        with st.container(border=True, key="card_budget"):
            st.subheader("Monthly Budget")
            if saved_budget is not None:
                share = used / saved_budget
                st.progress(min(share, 1.0), text=f"{share:.0%} of the budget used")
            st.text_input(
                "Budget for this month (RM)",
                value="" if saved_budget is None else f"{saved_budget:.2f}",
                key=f"budget_{selected_month}",
            )
            st.button(
                "Save budget",
                type="primary",
                on_click=save_budget_from_form,
                args=(selected_month,),
            )
            kind, text = st.session_state.pop("budget_feedback", (None, None))
            if kind == "error":
                st.error(text)
            elif kind == "success":
                st.success(text)
            if saved_budget is None:
                st.info("No budget set for this month.")

    if expenses.empty:
        chart_col.info("No MYR expenses in this month.")
    else:
        category_spending = expenses.groupby("category")["amount"].sum().abs()
        chart_data = category_spending.rename("Spending (RM)").reset_index()
        with chart_col:
            with st.container(border=True, key="card_chart"):
                st.subheader("Spending by Category")
                st.altair_chart(
                    alt.Chart(chart_data)
                    .mark_bar(color="#0F766E", cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
                    .encode(
                        x=alt.X("category:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
                        y=alt.Y("Spending (RM):Q", title="RM"),
                        tooltip=["category", alt.Tooltip("Spending (RM):Q", format=",.2f")],
                    )
                    .properties(height=440)
                    .configure(background="rgba(0,0,0,0)")
                    .configure_view(stroke=None)
                    .configure_axis(domain=False, ticks=False, gridColor="#EEF1F4", labelColor="#64748B"),
                    width="stretch",
                )
        with side_col:
            with st.container(border=True, key="card_table"):
                st.subheader("By category")
                st.dataframe(
                    chart_data,
                    hide_index=True,
                    column_config={"Spending (RM)": st.column_config.NumberColumn(format="%.2f")},
                )

    with st.container(border=True, key="card_transactions"):
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
    from exchange_rates import TARGET_CURRENCIES, get_rates

    today = date.today()
    transactions = st.session_state["transactions"]
    if transactions is None:
        transactions = pd.read_csv(SAMPLE_CSV, encoding="utf-8-sig")
        default_day = min(today, pd.to_datetime(transactions["date"]).max().date())
        st.caption("Sample transactions · import a CSV on the Transactions page to use your own.")
    else:
        default_day = today

    currency_col, day_col = st.columns(2)
    currency = currency_col.selectbox("Home currency", TARGET_CURRENCIES)
    as_of = day_col.date_input("Forecast as of", value=default_day, max_value=today)
    rates, rate_date, source = get_rates()
    quote = rates.get(currency)
    if quote is not None and (not isfinite(quote) or quote <= 0):
        quote = None
    if source == "Fallback data":
        st.warning("Using saved demo exchange rates. The live service is unavailable.")
    elif source == "Cached data":
        st.warning(f"Using the last saved exchange rates from {rate_date}.")
    else:
        st.caption(f"Exchange rates as of {rate_date} · Frankfurter")

    show_forecast(transactions, as_of, currency, quote)
    show_rate_alert(currency, quote, today)
