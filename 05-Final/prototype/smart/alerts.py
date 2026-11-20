from statistics import mean


def alert_triggered(current_rate, target_rate):
    """Trigger a transfer alert when the current rate reaches the target."""
    return current_rate >= target_rate


def default_target(rates):
    """Average the available daily rates, supplied oldest first."""
    recent_rates = rates[-30:]
    if not recent_rates:
        raise ValueError("At least one exchange rate is required.")
    return mean(recent_rates)
