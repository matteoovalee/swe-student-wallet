import re
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

APP = Path(__file__).parent.parent / "app.py"


def open_forecast_page():
    """Student on the Forecast and alerts page. The rates come from the saved CSV."""
    app = AppTest.from_file(str(APP), default_timeout=30)
    app.session_state["user_role"] = "student"
    app.run()
    app.sidebar.radio[0].set_value("Forecast and alerts").run()
    return app


def press(app, label):
    next(b for b in app.button if b.label == label).click().run()


def alert_messages(app):
    return [text.value for text in list(app.info) + list(app.success)]


def test_use_average_removes_the_saved_target():
    # TC-09: clearing the box and saving brought the old target back.
    with patch("urllib.request.urlopen", side_effect=OSError), \
            patch("exchange_rates.urlopen", side_effect=OSError):
        app = open_forecast_page()
        assert not app.exception
        app.number_input[0].set_value(9.0)
        press(app, "Save target")
        assert app.session_state["transfer_targets"] == {"EUR": 9.0}
        assert any("target of 9.0000" in text for text in alert_messages(app))

        press(app, "Use average")
        assert not app.exception
        assert "EUR" not in app.session_state["transfer_targets"]
        shown = [m.value for m in app.markdown if m.value.startswith("30-day average:")]
        average = re.search(r"([\d.]+) MYR", shown[0]).group(1)
        assert any(f"target of {average}" in text for text in alert_messages(app))
        assert not any("9.0000" in text for text in alert_messages(app))
