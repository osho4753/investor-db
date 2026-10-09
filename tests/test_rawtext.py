import urllib.error
import urllib.request
from datetime import date
from decimal import Decimal
from email.message import Message
from pathlib import Path

import pytest

import investor_db.rawtext as rawtext
from investor_db.rawtext import date_patterns, fetch_raw_text, find_first, html_to_text, money_patterns


class FakeResponse:
    def __init__(self, body: str) -> None:
        self.body = body.encode("utf-8")
        self.headers = Message()
        self.headers["Content-Type"] = "text/html; charset=utf-8"

    def read(self) -> bytes:
        return self.body

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None


def fake_opener(pages: dict[str, str]):
    requested: list[str] = []

    def opener(request: urllib.request.Request) -> FakeResponse:
        url = request.full_url
        requested.append(url)
        if url not in pages:
            raise urllib.error.HTTPError(url, 404, "Not Found", Message(), None)
        return FakeResponse(pages[url])

    opener.requested = requested
    return opener


@pytest.fixture(autouse=True)
def no_delay(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rawtext, "REQUEST_DELAY_SECONDS", 0)
    monkeypatch.setattr(rawtext.time, "sleep", lambda seconds: None)


def test_html_to_text_skips_scripts_and_collapses_whitespace() -> None:
    html = "<html><head><style>p{}</style><script>var x=1;</script></head><body><p>Fond\n  uzavřen</p><p>22 mil. EUR</p></body></html>"

    assert html_to_text(html) == "Fond uzavřen 22 mil. EUR"


def test_fetch_downloads_caches_and_reuses(tmp_path: Path) -> None:
    opener = fake_opener({"https://example.com/robots.txt": "User-agent: *\nDisallow:", "https://example.com/a": "<p>Text</p>"})

    first = fetch_raw_text("https://example.com/a", tmp_path, opener)
    second = fetch_raw_text("https://example.com/a", tmp_path, opener)

    assert (first.status, first.text) == ("staženo", "Text")
    assert (second.status, second.text) == ("z cache", "Text")
    assert opener.requested.count("https://example.com/a") == 1


def test_fetch_respects_robots_txt(tmp_path: Path) -> None:
    opener = fake_opener({"https://example.com/robots.txt": "User-agent: *\nDisallow: /"})

    page = fetch_raw_text("https://example.com/a", tmp_path, opener)

    assert page.status == "zakázáno v robots.txt" and not page.has_text
    assert "https://example.com/a" not in opener.requested


def test_fetch_reports_http_error_and_allows_missing_robots(tmp_path: Path) -> None:
    page = fetch_raw_text("https://example.com/missing", tmp_path, fake_opener({}))

    assert page.status == "HTTP 404" and not page.has_text


@pytest.mark.parametrize(
    ("amount", "text"),
    [
        (Decimal("1000000"), "Typical check: $1-5M per company"),
        (Decimal("5000000"), "Typical check: $1-5M per company"),
        (Decimal("3300000"), "raised 3,3 milionu USD v pre-seed kole"),
        (Decimal("250000"), "ticket €250K – €500K"),
        (Decimal("1200000000"), "cílová velikost 1,2 mld. Kč"),
        (Decimal("22000000"), "uzavřel fond ve výši 22 milionů eur"),
        (Decimal("500000000"), "AUM 500 000 000 USD"),
    ],
)
def test_money_patterns_find_common_notations(amount: Decimal, text: str) -> None:
    assert find_first(text, money_patterns(amount)) is not None


@pytest.mark.parametrize(
    ("amount", "text"),
    [
        (Decimal("1200000"), "cílová velikost 1,2 mld. Kč"),
        (Decimal("2000000"), "kolo 12 mil. EUR"),
    ],
)
def test_money_patterns_do_not_match_other_amounts(amount: Decimal, text: str) -> None:
    assert find_first(text, money_patterns(amount)) is None


@pytest.mark.parametrize(
    "text",
    ["dne 5. 11. 2025 oznámil", "November 5, 2025", "5 Nov 2025", "5. listopadu 2025", "2025-11-05", "5/11/2025"],
)
def test_date_patterns_find_common_notations(text: str) -> None:
    assert find_first(text, date_patterns(date(2025, 11, 5))) is not None


@pytest.mark.parametrize("text", ["duben 2026", "April 2026", "Apr 2026", "v dubnu 2026", "2026-04"])
def test_month_precision_patterns(text: str) -> None:
    expected = text != "v dubnu 2026"

    assert (find_first(text, date_patterns(date(2026, 4, 1), month_precision=True)) is not None) is expected


def test_date_patterns_do_not_match_other_day() -> None:
    assert find_first("15. 11. 2025", date_patterns(date(2025, 11, 5))) is None
