from io import BytesIO
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from exchange_rates import fetch_rates


# Saved Frankfurter v2 response excerpt, MYR base, 20 November 2026.
SAMPLE = b"""[
    {"date":"2026-11-20","base":"MYR","quote":"CNY","rate":1.6202},
    {"date":"2026-11-20","base":"MYR","quote":"EUR","rate":0.22135},
    {"date":"2026-11-20","base":"MYR","quote":"INR","rate":22.668},
    {"date":"2026-11-20","base":"MYR","quote":"SAR","rate":0.91185},
    {"date":"2026-11-20","base":"MYR","quote":"USD","rate":0.24316}
]"""


def test_fetch_rates_with_saved_response():
    with patch("exchange_rates.urlopen", return_value=BytesIO(SAMPLE)) as request:
        rates, rate_date = fetch_rates()

    request.assert_called_once()
    url = urlsplit(request.call_args.args[0])
    assert (url.scheme, url.netloc, url.path) == ("https", "api.frankfurter.dev", "/v2/rates")
    assert parse_qs(url.query) == {"base": ["MYR"], "quotes": ["EUR,USD,CNY,INR,SAR"]}
    assert rate_date == "2026-11-20"
    assert rates == {"EUR": 0.22135, "USD": 0.24316, "CNY": 1.6202,
                     "INR": 22.668, "SAR": 0.91185}
