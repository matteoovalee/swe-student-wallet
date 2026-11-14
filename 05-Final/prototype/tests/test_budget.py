import pytest

from smart.budget import budget_status, load_budget, parse_budget, save_budget


def test_parse_budget_accepts_numbers():
    assert parse_budget("2000") == 2000.0
    assert parse_budget(" 1,500.50 ") == 1500.5
    assert parse_budget("0.01") == 0.01


@pytest.mark.parametrize("text", ["", "   ", "abc", "0", "-5", "nan", "inf", None])
def test_parse_budget_rejects_bad_values(text):
    with pytest.raises(ValueError):
        parse_budget(text)


def test_budget_status_under_budget():
    assert budget_status(2000, 500) == (500, 1500)


def test_budget_status_over_budget_is_negative():
    used, left = budget_status(100, 150)
    assert used == 150
    assert left == -50


def test_budget_status_without_spending_has_no_negative_zero():
    used, left = budget_status(0.5, 0.5)
    assert str(left) == "0.0"
    used, left = budget_status(100, -0.0)
    assert str(used) == "0.0"


def test_budget_status_rounds_to_cents():
    assert budget_status(0.3, 0.1) == (0.1, 0.2)


def test_load_budget_without_file_returns_none(tmp_path):
    assert load_budget(tmp_path / "budgets.csv", "2026-10") is None


def test_save_and_load_budget(tmp_path):
    path = tmp_path / "budgets.csv"
    save_budget(path, "2026-10", 2000)
    assert load_budget(path, "2026-10") == 2000.0
    assert load_budget(path, "2026-09") is None
    assert path.read_text() == "month,amount_myr\n2026-10,2000.00\n"


def test_save_budget_replaces_the_same_month_and_keeps_the_others(tmp_path):
    path = tmp_path / "budgets.csv"
    save_budget(path, "2026-10", 2000)
    save_budget(path, "2026-09", 1800)
    save_budget(path, "2026-10", 2500.5)
    assert load_budget(path, "2026-10") == 2500.5
    assert load_budget(path, "2026-09") == 1800.0
    assert path.read_text().count("2026-10") == 1
