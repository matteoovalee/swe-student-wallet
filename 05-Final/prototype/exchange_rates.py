import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import streamlit as st

BASE_CURRENCY = "MYR"
TARGET_CURRENCIES = ["EUR", "USD", "CNY", "INR", "SAR"]

# Used only when the API is unavailable and nothing is cached yet.
# Demonstration values for 1 MYR, calculated from the frankfurter.dev rates of 25 Oct 2026.
# They are not real-time exchange rates.
DEMO_FALLBACK = {
    "EUR": 0.2183,
    "USD": 0.2449,
    "CNY": 1.6325,
    "INR": 23.21,
    "SAR": 0.9184,
}


@st.cache_data(ttl=3600)
def fetch_rates():
    query = urlencode({
        "base": BASE_CURRENCY,
        "quotes": ",".join(TARGET_CURRENCIES),
    })
    url = f"https://api.frankfurter.dev/v2/rates?{query}"
    with urlopen(url, timeout=10) as response:
        rows = json.loads(response.read().decode("utf-8"))
    rates = {row["quote"]: row["rate"] for row in rows}
    rate_date = rows[0]["date"] if rows else "Unknown"
    return rates, rate_date


def get_rates():
    try:
        rates, rate_date = fetch_rates()
        st.session_state["last_good_rates"] = (rates, rate_date)
        return rates, rate_date, "Live API data"
    except (URLError, TimeoutError, ValueError, KeyError, IndexError):
        if "last_good_rates" in st.session_state:
            rates, rate_date = st.session_state["last_good_rates"]
            return rates, rate_date, "Cached data"
        return DEMO_FALLBACK, "Demo values", "Fallback data"
