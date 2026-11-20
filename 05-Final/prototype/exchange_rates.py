"""Frankfurter reference rates, quoted as units of home currency for 1 MYR."""

import csv
import json
import logging
from datetime import date, timedelta
from http.client import HTTPException
from math import isfinite
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlencode
from urllib.request import urlopen

BASE_CURRENCY = "MYR"
TARGET_CURRENCIES = ["EUR", "USD", "CNY", "INR", "SAR"]
CACHE_FILE = Path(__file__).with_name("data") / "rates_cache.csv"
# Last resort if the saved CSV is missing or damaged.
DEMO_FALLBACK = {"EUR": 0.2183, "USD": 0.2449, "CNY": 1.6325, "INR": 23.21, "SAR": 0.9184}


def _download(**date_filters):
    query = urlencode({"base": BASE_CURRENCY, "quotes": ",".join(TARGET_CURRENCIES),
                       **date_filters})
    with urlopen(f"https://api.frankfurter.dev/v2/rates?{query}", timeout=10) as response:
        rows = json.load(response)

    history = {}
    for row in rows:
        if row["base"] != BASE_CURRENCY or row["quote"] not in TARGET_CURRENCIES:
            continue
        day = date.fromisoformat(row["date"])
        rate = float(row["rate"])
        if not isfinite(rate) or rate <= 0:
            raise ValueError("Invalid exchange rate")
        history.setdefault(day, {})[row["quote"]] = rate
    return history


def _latest(history):
    # A single displayed date must apply to all five quotes.
    complete_days = [day for day, quotes in history.items() if len(quotes) == len(TARGET_CURRENCIES)]
    day = max(complete_days, default=None)
    if day is None:
        raise ValueError("No complete daily quote available")
    return history[day], day.isoformat()


def fetch_rates():
    """Download the latest rates and their date without starting Streamlit."""
    return _latest(_download())


def fetch_rate_history(end):
    """Download available daily quotes in a 30-calendar-day window, inclusive."""
    start = end - timedelta(days=29)
    history = _download(**{"from": start.isoformat(), "to": end.isoformat()})
    return {day: quotes for day, quotes in history.items() if start <= day <= end}


def _read_cache():
    data = {}
    with CACHE_FILE.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            quotes = {c: float(row[c]) for c in TARGET_CURRENCIES if row[c]}
            if not all(isfinite(rate) and rate > 0 for rate in quotes.values()):
                raise ValueError("Invalid rate in saved CSV")
            data[date.fromisoformat(row["date"])] = quotes
    return data


def _write_cache(history):
    # A reader sees either the previous complete CSV or the replacement.
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=CACHE_FILE.parent, delete=False) as temp:
        path = Path(temp.name)
    try:
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["date", *TARGET_CURRENCIES])
            writer.writeheader()
            for day in sorted(history):
                writer.writerow({"date": day.isoformat(), **history[day]})
        path.replace(CACHE_FILE)
    finally:
        path.unlink(missing_ok=True)


def _refresh(end):
    rates, published = fetch_rates()
    day = date.fromisoformat(published)
    start = end - timedelta(days=29)
    if not start <= day <= end:
        raise ValueError("Latest quote falls outside the requested window")

    try:
        saved = _read_cache()
    except (OSError, ValueError, KeyError, TypeError, csv.Error):
        saved = {}
    history = {d: quotes for d, quotes in saved.items() if start <= d <= end}
    try:
        downloaded = fetch_rate_history(end)
    except (OSError, HTTPException, ValueError, TypeError, KeyError) as error:
        logging.getLogger(__name__).warning("Could not refresh historical rates: %s", error)
        downloaded = {}
    for d, quotes in downloaded.items():
        history.setdefault(d, {}).update(quotes)
    history[day] = rates
    try:
        _write_cache(history)
    except OSError as error:
        logging.getLogger(__name__).warning("Could not save exchange rates: %s", error)
    return history


def get_rates():
    """Streamlit adapter. Return (rates, rate date, source) as before."""
    import streamlit as st

    today = date.today()
    cached_refresh = st.cache_data(ttl=3600, show_spinner=False)(_refresh)
    try:
        history = cached_refresh(today)
        rates, rate_date = _latest(history)
        source = "Live API data"
    except (OSError, HTTPException, ValueError, TypeError, KeyError):
        try:
            history = _read_cache()
            rates, rate_date = _latest(history)
        except (OSError, ValueError, TypeError, KeyError, csv.Error):
            if "last_good_rates" in st.session_state:
                return (*st.session_state["last_good_rates"], "Cached data")
            return DEMO_FALLBACK.copy(), "Demo values", "Fallback data"
        source = "Cached data"

    st.session_state["last_good_rates"] = (rates, rate_date)
    # The alerts page compares MYR received for one unit of the home currency.
    start = today - timedelta(days=29)
    for currency in TARGET_CURRENCIES:
        st.session_state[f"transfer_history_{currency}"] = {
            day: 1 / quotes[currency] for day, quotes in history.items()
            if start <= day <= today and currency in quotes
        }
    return rates, rate_date, source
