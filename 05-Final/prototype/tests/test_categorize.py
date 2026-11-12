from smart.categorize import categorize


def test_grab_trip_is_transport():
    assert categorize("GRAB*TRIP") == "Transport"


def test_supermarket_is_food():
    assert categorize("NTUC FAIRPRICE") == "Food"


def test_spotify_is_subscription():
    assert categorize("SPOTIFY") == "Subscriptions"


def test_unknown_merchant_is_other():
    assert categorize("UNKNOWN MERCHANT") == "Other"
