import pytest

from smart.alerts import alert_triggered, default_target


def test_rate_below_target_does_not_trigger_alert():
    assert alert_triggered(4.99, 5.00) is False


def test_rate_equal_to_target_triggers_alert():
    assert alert_triggered(5.00, 5.00) is True


def test_rate_above_target_triggers_alert():
    assert alert_triggered(5.01, 5.00) is True


def test_default_target_is_the_average_of_thirty_rates():
    rates = [4.0, 5.0, 6.0] * 10
    assert default_target(rates) == pytest.approx(5.0)


def test_default_target_with_decimal_rates():
    assert default_target([4.8, 5.0, 5.2]) == pytest.approx(5.0)


def test_default_target_with_one_available_rate():
    assert default_target([4.75]) == pytest.approx(4.75)


def test_default_target_rejects_an_empty_list():
    # Proposed behaviour for review with Xiang: report invalid input
    # because an empty list has no average. Issue #35 leaves this open.
    with pytest.raises(ValueError):
        default_target([])
