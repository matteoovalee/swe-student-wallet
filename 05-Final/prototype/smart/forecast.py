def forecast_end_of_month(balance_myr, spent_myr, day_of_month, days_in_month):
    """Project the current MYR balance using this month's daily spending."""
    if not 1 <= day_of_month <= days_in_month:
        raise ValueError("The day must fall within the given month.")
    daily_spending = spent_myr / day_of_month
    remaining_days = days_in_month - day_of_month
    return balance_myr - daily_spending * remaining_days


def forecast_in_home_currency(balance_myr, spent_myr, day_of_month,
                              days_in_month, home_currency):
    """Convert the projected MYR balance using the prototype's current rate."""
    projected = forecast_end_of_month(balance_myr, spent_myr, day_of_month, days_in_month)
    if home_currency == "MYR":
        return projected

    from exchange_rates import get_rates

    rates, _, _ = get_rates()
    return projected * rates[home_currency]
