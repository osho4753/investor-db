import json
from decimal import Decimal
from pathlib import Path

from investor_db.__main__ import main
from investor_db.tokens import PRICES, render_usage, session_usage


def assistant(message_id: str, usage: dict, tools: tuple[str, ...] = ()) -> dict:
    content = [{"type": "tool_use", "name": name} for name in tools]
    return {"type": "assistant", "message": {"id": message_id, "model": "claude-opus-5-5", "usage": usage, "content": content}}


USAGE = {
    "input_tokens": 10,
    "output_tokens": 1000,
    "output_tokens_details": {"thinking_tokens": 300},
    "cache_read_input_tokens": 100000,
    "cache_creation_input_tokens": 2000,
    "cache_creation": {"ephemeral_5m_input_tokens": 500, "ephemeral_1h_input_tokens": 1500},
}
COST_STATE = {
    "type": "cost-state",
    "modelUsage": {
        "claude-opus-5-5": {"inputTokens": 999},
        "claude-haiku-5-5": {"inputTokens": 20000, "outputTokens": 1000, "thinkingTokens": 400, "webSearchRequests": 2},
    },
}


def write_transcript(path: Path) -> Path:
    rows = [
        {"type": "user", "message": {"content": "úkol"}},
        assistant("msg-1", USAGE, ("WebFetch",)),
        assistant("msg-1", USAGE, ("WebSearch",)),
        assistant("msg-2", {"input_tokens": 5, "output_tokens": 200, "cache_read_input_tokens": 50000}),
        COST_STATE,
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
    return path


def test_response_counted_once_per_message_id(tmp_path: Path) -> None:
    usage = session_usage([write_transcript(tmp_path / "s.jsonl")])
    opus = usage.models["claude-opus-5-5"]

    assert (opus.responses, opus.input, opus.output, opus.thinking, opus.read) == (2, 15, 1200, 300, 150000)
    assert (opus.write_5m, opus.write_1h) == (500, 1500)
    assert usage.tools == {"WebFetch": 1, "WebSearch": 1}


def test_tool_models_come_from_cost_state(tmp_path: Path) -> None:
    haiku = session_usage([write_transcript(tmp_path / "s.jsonl")]).models["claude-haiku-5-5"]

    assert (haiku.input, haiku.output, haiku.web_searches) == (20000, 1000, 2)


def test_cost_uses_price_per_token_type(tmp_path: Path) -> None:
    usage = session_usage([write_transcript(tmp_path / "s.jsonl")])
    opus = PRICES["claude-opus-5-5"]
    haiku = PRICES["claude-haiku-5-5"]
    expected_opus = (15 * opus.input + 500 * opus.write_5m + 1500 * opus.write_1h + 150000 * opus.read + 1200 * opus.output) / Decimal(1_000_000)
    expected_haiku = (20000 * haiku.input + 1000 * haiku.output) / Decimal(1_000_000) + Decimal("0.02")

    assert usage.cost() == expected_opus + expected_haiku


def test_render_reports_per_investor(tmp_path: Path) -> None:
    text = render_usage(session_usage([write_transcript(tmp_path / "s.jsonl")]), 3)

    assert "Na investora (n = 3)" in text
    assert "claude-haiku-5-5" in text


def test_cli_prints_usage(tmp_path: Path, capsys) -> None:
    assert main(["tokens", str(write_transcript(tmp_path / "s.jsonl")), "--investors", "1"]) == 0
    assert "Celkem 174215 tokenů" in capsys.readouterr().out
