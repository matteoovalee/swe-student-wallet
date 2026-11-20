import pytest

from smart.forecast import forecast_end_of_month


def test_forecast_matches_the_issue_example():
    # Daily spending is 300 / 10 = 30. There are 20 days left.
    # Expected balance is 1000 - (30 * 20) = 400.
    result = forecast_end_of_month(1000, 300, 10, 30)
    assert result == pytest.approx(400)


def test_forecast_on_the_first_day():
    # Spending 10 on day 1 leaves 29 days at the same daily rate.
    result = forecast_end_of_month(1000, 10, 1, 30)
    assert result == pytest.approx(710)


def test_forecast_on_the_last_day():
    # There are zero days left, so the current balance stays the same.
    result = forecast_end_of_month(1000, 300, 30, 30)
    assert result == pytest.approx(1000)


def test_forecast_with_zero_spending():
    result = forecast_end_of_month(1000, 0, 10, 30)
    assert result == pytest.approx(1000)


def test_forecast_can_show_a_shortfall():
    # 100 - (30 * 20) = -500.
    result = forecast_end_of_month(100, 300, 10, 30)
    assert result == pytest.approx(-500)


def test_forecast_uses_the_given_month_length():
    # Daily spending is 20, with 14 days left in a 28-day month.
    result = forecast_end_of_month(1000, 280, 14, 28)
    assert result == pytest.approx(720)
