# Prototype

Python and Streamlit. It is an evolutionary prototype: it starts small and grows sprint by sprint.

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
