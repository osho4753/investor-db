from datetime import date
from decimal import Decimal

import pytest

from investor_db.values import (
    is_valid_country,
    is_valid_ico,
    is_valid_url,
    normalize_name,
    parse_date,
    parse_money,
    split_list,
    website_domain,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("2026-01-31", date(2026, 1, 31)),
        ("2026-02-30", None),
        ("20260131", None),
        ("31.1.2026", None),
        ("", None),
    ],
)
def test_parse_date(text: str, expected: date | None) -> None:
    assert parse_date(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1000000", Decimal("1000000")),
        ("2.5", Decimal("2.5")),
        ("-5", None),
        ("1 000", None),
        ("1,5", None),
        ("1e6", None),
        ("", None),
    ],
)
def test_parse_money(text: str, expected: Decimal | None) -> None:
    assert parse_money(text) == expected


def test_split_list_ignores_whitespace_and_empty_items() -> None:
    assert split_list(" seed ; serie_a;;") == ["seed", "serie_a"]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("https://example.com", True),
        ("http://example.com/cesta?x=1", True),
        ("example.com", False),
        ("ftp://example.com", False),
        ("https://example.com/s mezerou", False),
    ],
)
def test_is_valid_url(text: str, expected: bool) -> None:
    assert is_valid_url(text) is expected


def test_website_domain_drops_www_and_path() -> None:
    assert website_domain("https://www.Example.com/o-nas") == "example.com"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("12345679", True),
        ("12345678", False),
        ("1234567", False),
        ("1234567a", False),
    ],
)
def test_is_valid_ico_checks_length_and_check_digit(text: str, expected: bool) -> None:
    assert is_valid_ico(text) is expected


@pytest.mark.parametrize(("text", "expected"), [("CZ", True), ("cz", False), ("CZE", False)])
def test_is_valid_country(text: str, expected: bool) -> None:
    assert is_valid_country(text) is expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Fiktivní Ventures a.s.", "fiktivni ventures"),
        ("FIKTIVNI VENTURES, s.r.o.", "fiktivni ventures"),
        ("Fiktivní-Ventures SICAV, a.s.", "fiktivni ventures"),
        ("Atlas Kapitál", "atlas kapital"),
    ],
)
def test_normalize_name_removes_diacritics_case_and_legal_form(name: str, expected: str) -> None:
    assert normalize_name(name) == expected
