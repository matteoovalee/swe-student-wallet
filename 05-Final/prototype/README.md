# Prototype

Python and Streamlit. It is an evolutionary prototype: it starts small and grows sprint by sprint.

## Live app

https://swe-student-wallet-group4.streamlit.app/ (deployed from `main` on Streamlit Community Cloud).

## Run it

```
cd 05-Final/prototype
pip install -r requirements.txt
streamlit run app.py
```

## Run the tests

```
pip install pytest
pytest
```

## Where things are

- `app.py`: the screens
- `smart/`: the smart features (categories, forecast, rate alert)
- `exchange_rates.py`: exchange rates from frankfurter.dev, with a cached fallback
- `tests/`: pytest tests
- `data/`: simulated demo data

## Demo Login Accounts

The application includes three fictional demo accounts for testing.

| Role | Email | Password |
|---|---|---|
| Student | student@example.com | StudentDemo2026! |
| Sponsor | sponsor@example.com | SponsorDemo2026! |
| Admin | admin@example.com | AdminDemo2026! |

### Access Permissions

- Student: Dashboard, Transactions, Forecast and alerts.
- Sponsor: Dashboard only, with read-only access.
- Admin: Access to all existing application pages.

Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes in data/users.csv.

These credentials are for demonstration purposes only.
