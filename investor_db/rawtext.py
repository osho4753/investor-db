import hashlib
import re
import time
import urllib.error
import urllib.request
import urllib.robotparser
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from typing import Final, Protocol
from urllib.parse import urlparse

USER_AGENT: Final = "investor-db-research/0.1 (rucni overeni jednotlivych faktu)"
REQUEST_DELAY_SECONDS: Final = 1.0
TIMEOUT_SECONDS: Final = 20
SKIPPED_TAGS: Final = frozenset({"script", "style", "noscript", "template"})

SCALES: Final = (
    (Decimal(10) ** 9, r"(?:mld\.?|miliard\w*|bn|billion|b\b)"),
    (Decimal(10) ** 6, r"(?:mil(?!iard)\w*\.?|mio\.?|million|m\b)"),
    (Decimal(10) ** 3, r"(?:tis\w*\.?|thousand|k\b)"),
)
RANGE_TAIL: Final = r"(?:\s*[-–]\s*[$€£]?\s*[\d.,]+)?\s*"

ENGLISH_MONTHS: Final = (
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
)
CZECH_MONTHS_NOMINATIVE: Final = (
    "leden", "únor", "březen", "duben", "květen", "červen",
    "červenec", "srpen", "září", "říjen", "listopad", "prosinec",
)
CZECH_MONTHS_GENITIVE: Final = (
    "ledna", "února", "března", "dubna", "května", "června",
    "července", "srpna", "září", "října", "listopadu", "prosince",
)


class Response(Protocol):
    headers: object

    def read(self) -> bytes: ...

    def __enter__(self) -> "Response": ...

    def __exit__(self, *args: object) -> None: ...


Opener = Callable[[urllib.request.Request], Response]


@dataclass(frozen=True)
class RawPage:
    url: str
    status: str
    text: str

    @property
    def has_text(self) -> bool:
        return bool(self.text.strip())


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SKIPPED_TAGS:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIPPED_TAGS and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip_depth and data.strip():
            self.parts.append(data.strip())


def html_to_text(html: str) -> str:
    extractor = TextExtractor()
    extractor.feed(html)
    return re.sub(r"\s+", " ", " ".join(extractor.parts))


def default_opener(request: urllib.request.Request) -> Response:
    return urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS)


def download(url: str, opener: Opener) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with opener(request) as response:
        body = response.read()
        charset = getattr(response.headers, "get_content_charset", lambda: None)() or "utf-8"
    return body.decode(charset, errors="replace")


def robots_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}/robots.txt"


def is_allowed_by_robots(url: str, opener: Opener) -> bool:
    parser = urllib.robotparser.RobotFileParser()
    try:
        parser.parse(download(robots_url(url), opener).splitlines())
    except (urllib.error.URLError, TimeoutError, ValueError):
        return True
    return parser.can_fetch(USER_AGENT, url)


def cache_path(cache_dir: Path, url: str) -> Path:
    return cache_dir / f"{hashlib.sha256(url.encode('utf-8')).hexdigest()}.txt"


def fetch_raw_text(url: str, cache_dir: Path, opener: Opener = default_opener) -> RawPage:
    cached = cache_path(cache_dir, url)
    if cached.exists():
        return RawPage(url, "z cache", cached.read_text(encoding="utf-8"))
    if not is_allowed_by_robots(url, opener):
        return RawPage(url, "zakázáno v robots.txt", "")
    try:
        text = html_to_text(download(url, opener))
    except urllib.error.HTTPError as error:
        return RawPage(url, f"HTTP {error.code}", "")
    except (urllib.error.URLError, TimeoutError, ValueError) as error:
        return RawPage(url, f"chyba spojení: {error}", "")
    finally:
        time.sleep(REQUEST_DELAY_SECONDS)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cached.write_text(text, encoding="utf-8")
    return RawPage(url, "staženo", text)


def number_variants(number: Decimal) -> list[str]:
    plain = format(number.normalize(), "f")
    if "." in plain:
        plain = plain.rstrip("0").rstrip(".")
    return sorted({plain, plain.replace(".", ",")}, key=len, reverse=True)


def grouped_variants(amount: Decimal) -> list[str]:
    if amount != amount.to_integral_value():
        return []
    digits = f"{int(amount):,}"
    return sorted({digits, digits.replace(",", " "), digits.replace(",", "."), digits.replace(",", "")}, key=len, reverse=True)


def money_patterns(amount: Decimal) -> list[re.Pattern[str]]:
    patterns = [re.compile(rf"(?<![\d.,]){re.escape(variant)}(?![\d])") for variant in grouped_variants(amount) if len(variant) > 3]
    for scale, unit in SCALES:
        scaled = amount / scale
        if scaled >= Decimal("0.1"):
            for variant in number_variants(scaled):
                patterns.append(re.compile(rf"(?<![\d.,]){re.escape(variant)}{RANGE_TAIL}{unit}", re.IGNORECASE))
    return patterns


def date_patterns(day: date, month_precision: bool = False) -> list[re.Pattern[str]]:
    english = ENGLISH_MONTHS[day.month - 1]
    czech = f"(?:{CZECH_MONTHS_NOMINATIVE[day.month - 1]}|{CZECH_MONTHS_GENITIVE[day.month - 1]})"
    if month_precision:
        sources = [
            rf"{english[:3]}\w*\.?\s+{day.year}",
            rf"{czech}\s+{day.year}",
            rf"{day.year}-{day.month:02d}",
            rf"\b0?{day.month}\s*/\s*{day.year}",
        ]
    else:
        sources = [
            rf"{day.isoformat()}",
            rf"\b0?{day.day}\.\s*0?{day.month}\.\s*{day.year}",
            rf"\b0?{day.day}/0?{day.month}/{day.year}",
            rf"\b0?{day.month}/0?{day.day}/{day.year}",
            rf"{english[:3]}\w*\.?\s+0?{day.day},?\s+{day.year}",
            rf"\b0?{day.day}(?:st|nd|rd|th)?\s+{english[:3]}\w*\.?,?\s+{day.year}",
            rf"\b0?{day.day}\.\s*{czech}\s+{day.year}",
        ]
    return [re.compile(source, re.IGNORECASE) for source in sources]


def find_first(text: str, patterns: list[re.Pattern[str]], width: int = 60) -> str | None:
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            start = max(0, match.start() - width)
            return text[start : match.end() + width]
    return None
