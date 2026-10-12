import html
import posixpath
import re
from dataclasses import dataclass

REPOSITORY_URL = "https://github.com/osho4753/investor-db"
BLOB_URL = f"{REPOSITORY_URL}/blob/main/"
TREE_URL = f"{REPOSITORY_URL}/tree/main/"

INLINE_PATTERN = re.compile(r"`([^`]+)`|\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)\s]+)\)")
REPOSITORY_LINK_PATTERN = re.compile(rf"{re.escape(REPOSITORY_URL)}/(?:blob|tree)/main/([^\"#?]+)")
TABLE_SEPARATOR = re.compile(r"^\|(\s*:?-+:?\s*\|)+$")


@dataclass(frozen=True)
class TimelineEntry:
    label: str
    title: str
    text: str


def repository_url(path: str) -> str:
    clean = path.rstrip("/")
    return (TREE_URL if path.endswith("/") else BLOB_URL) + clean


def resolve_link(target: str, base_dir: str) -> str:
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return target
    path, _, anchor = target.partition("#")
    normalized = posixpath.normpath(posixpath.join(base_dir, path))
    url = repository_url(("" if normalized == "." else normalized) + ("/" if path.endswith("/") else ""))
    return f"{url}#{anchor}" if anchor else url


def inline(text: str, base_dir: str = "") -> str:
    parts: list[str] = []
    position = 0
    for match in INLINE_PATTERN.finditer(text):
        parts.append(html.escape(text[position:match.start()]))
        code, bold, label, target = match.groups()
        if code is not None:
            parts.append(f"<code>{html.escape(code)}</code>")
        elif bold is not None:
            parts.append(f"<b>{inline(bold, base_dir)}</b>")
        else:
            parts.append(f'<a href="{html.escape(resolve_link(target, base_dir))}">{inline(label, base_dir)}</a>')
        position = match.end()
    parts.append(html.escape(text[position:]))
    return "".join(parts)


def paragraphs(text: str) -> list[list[str]]:
    return [block.strip().splitlines() for block in re.split(r"\n\s*\n", text.strip()) if block.strip()]


def render_block(lines: list[str], base_dir: str) -> str:
    if lines[0].startswith("### "):
        rest = render_block(lines[1:], base_dir) if lines[1:] else ""
        return f"<h4>{inline(lines[0][4:], base_dir)}</h4>{rest}"
    if all(line.startswith("- ") for line in lines):
        items = "".join(f"<li>{inline(line[2:], base_dir)}</li>" for line in lines)
        return f'<ul class="clean">{items}</ul>'
    return f"<p>{inline(' '.join(lines), base_dir)}</p>"


def render_text(text: str, base_dir: str = "") -> str:
    return "\n".join(render_block(lines, base_dir) for lines in paragraphs(text))


def timeline_entries(text: str) -> list[TimelineEntry]:
    entries = []
    for lines in paragraphs(text):
        label, _, title = lines[0].removeprefix("### ").partition("|")
        entries.append(TimelineEntry(label.strip(), title.strip(), " ".join(lines[1:])))
    return entries


def section_lines(markdown: str, heading: str) -> list[str]:
    lines = markdown.splitlines()
    start = next(index for index, line in enumerate(lines) if line.strip() == heading)
    level = len(heading) - len(heading.lstrip("#"))
    body = []
    for line in lines[start + 1:]:
        stripped = line.lstrip()
        if stripped.startswith("#") and len(stripped) - len(stripped.lstrip("#")) <= level:
            break
        body.append(line)
    return body


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split(" | ")]


def first_table(lines: list[str]) -> list[list[str]]:
    rows = []
    for line in lines:
        if line.startswith("|"):
            if not TABLE_SEPARATOR.match(line.strip()):
                rows.append(split_row(line))
        elif rows:
            break
    return rows


def render_table(rows: list[list[str]], base_dir: str = "") -> str:
    header, *body = rows
    head = "".join(f"<th>{inline(cell, base_dir)}</th>" for cell in header)
    lines = "".join("<tr>" + "".join(f"<td>{inline(cell, base_dir)}</td>" for cell in row) + "</tr>" for row in body)
    return f'<div class="tablewrap"><table><thead><tr>{head}</tr></thead><tbody>{lines}</tbody></table></div>'


def repository_paths(document: str) -> set[str]:
    return set(REPOSITORY_LINK_PATTERN.findall(document))
