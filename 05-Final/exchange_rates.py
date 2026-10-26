import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import streamlit as st


BASE_CURRENCY = "SGD"
TARGET_CURRENCIES = ["USD", "MYR", "EUR"]

# For demonstration purposes only—to be used when the API is unavailable; these are not real-time exchange rates.
DEMO_FALLBACK = {
    "USD": 0.74,
    "MYR": 3.30,
    "EUR": 0.68,
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
