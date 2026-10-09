import re
import unicodedata
from datetime import date
from decimal import Decimal
from urllib.parse import urlparse

from investor_db.schema import LIST_SEPARATOR

DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")
MONEY_PATTERN = re.compile(r"\d+(\.\d+)?")
ICO_PATTERN = re.compile(r"\d{8}")
COUNTRY_PATTERN = re.compile(r"[A-Z]{2}")
LEGAL_FORM_SUFFIX = re.compile(
    r"[\s,]+(a\.?\s?s\.?|s\.?\s?r\.?\s?o\.?|spol\.?\s?s\s?r\.?\s?o\.?|k\.?\s?s\.?|v\.?\s?o\.?\s?s\.?|se|sicav)$"
)
NON_ALPHANUMERIC = re.compile(r"[^a-z0-9]+")
ICO_WEIGHTS = (8, 7, 6, 5, 4, 3, 2)


def parse_date(text: str) -> date | None:
    if not DATE_PATTERN.fullmatch(text):
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def parse_money(text: str) -> Decimal | None:
    if not MONEY_PATTERN.fullmatch(text):
        return None
    return Decimal(text)


def split_list(text: str) -> list[str]:
    return [item.strip() for item in text.split(LIST_SEPARATOR) if item.strip()]


def is_valid_url(text: str) -> bool:
    parsed = urlparse(text)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc) and " " not in text


def website_domain(url: str) -> str:
    hostname = urlparse(url).hostname or ""
    return hostname.removeprefix("www.")


def is_valid_ico(text: str) -> bool:
    if not ICO_PATTERN.fullmatch(text):
        return False
    weighted_sum = sum(int(digit) * weight for digit, weight in zip(text, ICO_WEIGHTS))
    expected_check_digit = (11 - weighted_sum % 11) % 10
    return int(text[-1]) == expected_check_digit


def is_valid_country(text: str) -> bool:
    return bool(COUNTRY_PATTERN.fullmatch(text))


def strip_diacritics(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def normalize_name(name: str) -> str:
    simplified = strip_diacritics(name).casefold().strip()
    previous = None
    while previous != simplified:
        previous = simplified
        simplified = LEGAL_FORM_SUFFIX.sub("", simplified)
    return NON_ALPHANUMERIC.sub(" ", simplified).strip()
