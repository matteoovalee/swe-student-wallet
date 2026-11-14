from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).parent.parent / "app.py"
BUDGET_CSV = Path(__file__).parent.parent / "data" / "budgets.csv"


@pytest.fixture(autouse=True)
def keep_budget_file():
    """The tests save budgets: put the file back as it was when the test ends."""
    original = BUDGET_CSV.read_bytes() if BUDGET_CSV.exists() else None
    yield
    if original is None:
        BUDGET_CSV.unlink(missing_ok=True)
    else:
        BUDGET_CSV.write_bytes(original)


def run_dashboard():
    app = AppTest.from_file(str(APP), default_timeout=30)
    app.run()
    return app


def metrics(app):
    return {metric.label: metric.value for metric in app.metric}


def test_dashboard_shows_the_saved_budget_of_the_sample_month():
    app = run_dashboard()
    assert not app.exception
    values = metrics(app)
    assert values["Budget"] == "RM 2,000.00"
    assert values["Used"] == "RM 1,855.00"
    assert values["Left"] == "RM 145.00"


def test_save_a_new_budget():
    app = run_dashboard()
    app.text_input(key="budget_2026-10").input("2500")
    app.button[0].click().run()
    assert not app.exception
    assert app.success[0].value == "Budget saved."
    assert metrics(app)["Left"] == "RM 645.00"
    assert "2026-10,2500.00" in BUDGET_CSV.read_text()


def test_budget_below_spending_shows_a_negative_amount_left():
    app = run_dashboard()
    app.text_input(key="budget_2026-10").input("1800")
    app.button[0].click().run()
    assert not app.exception
    assert any("-55.00" in markdown.value for markdown in app.markdown)


@pytest.mark.parametrize("text", ["", "abc", "0", "-100"])
def test_bad_budget_shows_an_error_and_saves_nothing(text):
    before = BUDGET_CSV.read_text()
    app = run_dashboard()
    app.text_input(key="budget_2026-10").input(text)
    app.button[0].click().run()
    assert not app.exception
    assert app.error[0].value == "Enter an amount above zero, for example 2000."
    assert BUDGET_CSV.read_text() == before
    assert metrics(app)["Budget"] == "RM 2,000.00"


def test_month_without_budget_shows_a_message():
    app = run_dashboard()
    app.selectbox[0].select("2026-09").run()
    assert not app.exception
    assert any("No budget set for this month." in info.value for info in app.info)
