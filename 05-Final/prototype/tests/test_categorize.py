import pytest

from smart.categorize import categorize


@pytest.mark.parametrize(
    ("merchant", "expected"),
    [
        ("UNIVERSITY BOOKSTORE", "Education"),
        ("SHOPEE", "Shopping"),
        ("RAPID KL", "Transport"),
        ("GRAB*TRIP", "Transport"),
        ("MCDONALDS", "Food"),
        ("LOTUS'S", "Food"),
        ("FAMILYMART", "Food"),
        ("CAMPUS CAFE", "Food"),
        ("LAUNDRY SERVICE", "Other"),
        ("TEALIVE", "Food"),
        ("MYDIN", "Food"),
        ("7-ELEVEN", "Food"),
        ("TOUCH N GO", "Transport"),
        ("PHARMACY", "Other"),
        ("PHONE DATA PLAN", "Subscriptions"),
        ("TRANSFER FROM HOME", "Transfer"),
        ("MONTHLY RENT", "Rent"),
        ("PRINT SHOP", "Education"),
        ("CINEMA", "Other"),
        ("NETFLIX", "Subscriptions"),
    ],
)
def test_categorize_transaction_merchants(merchant, expected):
    assert categorize(merchant) == expected
