import csv
import math
from pathlib import Path


def parse_budget(text):
    """Turn the text typed by the student into a budget in MYR.

    Raises ValueError if the text is empty, not a number or not above zero.
    """
    try:
        value = float(str(text).strip().replace(",", ""))
    except ValueError:
        value = None

    if value is None or not math.isfinite(value) or value <= 0:
        raise ValueError("Enter an amount above zero, for example 2000.")
    return value


def budget_status(budget, spent):
    """Return (used, left) in MYR. Left is negative when the spending is above the budget."""
    used = round(spent, 2) + 0.0  # + 0.0 turns -0.0 into 0.0
    left = round(budget - spent, 2) + 0.0
    return used, left


def load_budget(path, month):
    """Return the budget saved for a month ("2026-10") or None."""
    path = Path(path)
    if not path.exists():
        return None

    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            if row["month"] == month:
                return float(row["amount_myr"])
    return None


def save_budget(path, month, amount):
    """Save the budget of a month. A budget saved before for the same month is replaced."""
    path = Path(path)
    budgets = {}

    if path.exists():
        with path.open(newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                budgets[row["month"]] = row["amount_myr"]

    budgets[month] = f"{amount:.2f}"

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["month", "amount_myr"])
        for saved_month in sorted(budgets):
            writer.writerow([saved_month, budgets[saved_month]])
