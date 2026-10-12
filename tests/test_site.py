import shutil
from pathlib import Path

import pytest
from conftest import build_valid_dataset
from test_cli import write_dataset

from investor_db.__main__ import main
from investor_db.markup import (
    first_table,
    inline,
    render_text,
    repository_paths,
    resolve_link,
    section_lines,
    timeline_entries,
)
from investor_db.schema import CATEGORY_EXCLUSION_REASONS, FACT_FIELDS
from investor_db.schema import INVESTOR_TYPES
from investor_db.site import ERRORS_HEADING, FIELD_LABELS, REASON_LABELS, SITE_DIR, SUMMARY_HEADING, TEXTS_DIR, TYPE_LABELS, build_site, verified_table

ROOT = Path(__file__).resolve().parents[1]

FIXTURE_README = f"""# Fiktivní projekt

{ERRORS_HEADING}

| # | Chyba | Jak se našla | Oprava |
|---|---|---|---|
| 1 | **Fiktivní chyba** v `kódu` | kontrolou | opraveno, viz [docs/02](docs/02-metodika.md) |

## Další oddíl
"""

FIXTURE_ESTIMATE = f"""# Odhad

{SUMMARY_HEADING}

| Kategorie | Svět |
|---|---|
| VC | 10 [M] |
"""


@pytest.fixture
def site_root(tmp_path: Path) -> Path:
    (tmp_path / "data").mkdir()
    write_dataset(tmp_path / "data", build_valid_dataset())
    shutil.copytree(ROOT / TEXTS_DIR, tmp_path / TEXTS_DIR)
    (tmp_path / "docs").mkdir()
    (tmp_path / "README.md").write_text(FIXTURE_README, encoding="utf-8")
    (tmp_path / "docs" / "03-globalni-odhad.md").write_text(FIXTURE_ESTIMATE, encoding="utf-8")
    return tmp_path


def test_committed_site_matches_regenerated_output() -> None:
    expected = build_site(ROOT)

    committed = {path.name: path.read_text(encoding="utf-8") for path in (ROOT / SITE_DIR).iterdir() if path.is_file()}

    assert committed.keys() == expected.keys()
    for name, content in expected.items():
        assert committed[name] == content, f"{SITE_DIR}/{name} není aktuální, spusť python -m investor_db site"


def test_repository_links_on_site_point_to_existing_files() -> None:
    pages = build_site(ROOT)
    paths = {path for name in ("index.html", "data.html") for path in repository_paths(pages[name])}

    assert paths
    assert [path for path in sorted(paths) if not (ROOT / path.rstrip("/")).exists()] == []


def test_site_is_built_from_dataset(site_root: Path) -> None:
    pages = build_site(site_root)

    assert pages["data.html"].count('<details class="inv"') == 3
    assert "Fiktivní Ventures" in pages["data.html"]
    assert "f-00008" in pages["data.html"]
    assert "R1 vzorek: správně" in pages["data.html"]
    assert "chyba 1" in pages["data.html"]
    assert "<td>10 [M]</td>" in pages["index.html"]
    assert "1/1" in pages["index.html"]


def test_verified_table_is_generated_from_data() -> None:
    table = verified_table(build_valid_dataset())

    assert "Ověření investoři (1)" in table
    assert "<td class=\"mono\">12345679</td><td>VC</td><td>Fiktivní Startup s.r.o. (2025-11-15)</td>" in table
    assert 'href="https://' in table


def test_site_command_writes_files(site_root: Path) -> None:
    output = site_root / "out"

    assert main(["--data-dir", str(site_root / "data"), "site", "--output", str(output)]) == 0

    assert sorted(path.name for path in output.iterdir()) == ["app.js", "data.html", "index.html", "style.css"]


def test_labels_cover_vocabularies() -> None:
    assert set(FACT_FIELDS) <= FIELD_LABELS.keys()
    assert set(CATEGORY_EXCLUSION_REASONS) <= REASON_LABELS.keys()
    assert set(INVESTOR_TYPES) <= TYPE_LABELS.keys()


@pytest.mark.parametrize(
    ("target", "base_dir", "expected"),
    [
        ("docs/04-rucni-kontrola.md", "", "https://github.com/osho4753/investor-db/blob/main/docs/04-rucni-kontrola.md"),
        ("01-plan-a-kriteria.md", "docs", "https://github.com/osho4753/investor-db/blob/main/docs/01-plan-a-kriteria.md"),
        ("../README.md#práce-s-ai", "ai-log", "https://github.com/osho4753/investor-db/blob/main/README.md#práce-s-ai"),
        ("ai-log/", "", "https://github.com/osho4753/investor-db/tree/main/ai-log"),
        ("https://example.org/a", "docs", "https://example.org/a"),
    ],
)
def test_links_resolve_to_repository(target: str, base_dir: str, expected: str) -> None:
    assert resolve_link(target, base_dir) == expected


def test_inline_markup_escapes_html() -> None:
    assert inline("**a** `<b>` [x](https://e.org) & <i>") == '<b>a</b> <code>&lt;b&gt;</code> <a href="https://e.org">x</a> &amp; &lt;i&gt;'


def test_text_blocks_and_tables_are_parsed() -> None:
    text = "### Nadpis\n- jedna\n- dvě\n\nOdstavec\npokračuje."

    assert render_text(text) == '<h4>Nadpis</h4><ul class="clean"><li>jedna</li><li>dvě</li></ul>\n<p>Odstavec pokračuje.</p>'
    assert first_table(section_lines(FIXTURE_ESTIMATE, SUMMARY_HEADING)) == [["Kategorie", "Svět"], ["VC", "10 [M]"]]
    assert timeline_entries("### 9. 10. | Plán\nText.")[0].title == "Plán"
