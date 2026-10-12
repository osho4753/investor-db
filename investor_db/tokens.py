import json
from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Final, Iterable

PRICE_SOURCE: Final = "https://platform.claude.com/docs/en/about-claude/pricing"
PRICE_ACCESSED: Final = "2026-10-13"
MILLION: Final = Decimal(1_000_000)
WEB_SEARCH_USD: Final = Decimal("0.01")


@dataclass(frozen=True)
class Price:
    input: Decimal
    write_5m: Decimal
    write_1h: Decimal
    read: Decimal
    output: Decimal


PRICES: Final = {
    "claude-opus-5-5": Price(Decimal("4"), Decimal("5"), Decimal("8"), Decimal("0.20"), Decimal("20")),
    "claude-haiku-5-5": Price(Decimal("0.10"), Decimal("0.125"), Decimal("0.20"), Decimal("0.01"), Decimal("0.50")),
}


@dataclass
class ModelUsage:
    input: int = 0
    output: int = 0
    thinking: int = 0
    read: int = 0
    write_5m: int = 0
    write_1h: int = 0
    web_searches: int = 0
    responses: int = 0

    @property
    def total(self) -> int:
        return self.input + self.output + self.read + self.write_5m + self.write_1h

    def cost(self, price: Price) -> Decimal:
        tokens = (
            self.input * price.input
            + self.write_5m * price.write_5m
            + self.write_1h * price.write_1h
            + self.read * price.read
            + self.output * price.output
        )
        return tokens / MILLION + self.web_searches * WEB_SEARCH_USD


@dataclass
class SessionUsage:
    models: dict[str, ModelUsage] = field(default_factory=dict)
    tools: Counter[str] = field(default_factory=Counter)

    @property
    def total_tokens(self) -> int:
        return sum(usage.total for usage in self.models.values())

    def cost(self) -> Decimal:
        return sum((usage.cost(PRICES[model]) for model, usage in self.models.items()), Decimal(0))


def records(lines: Iterable[str]) -> Iterable[dict]:
    for line in lines:
        if line.strip():
            yield json.loads(line)


def response_usage(usage: dict) -> ModelUsage:
    cache = usage.get("cache_creation") or {}
    write_5m = cache.get("ephemeral_5m_input_tokens", 0)
    write_1h = cache.get("ephemeral_1h_input_tokens", 0)
    if not cache:
        write_5m = usage.get("cache_creation_input_tokens", 0)
    return ModelUsage(
        input=usage.get("input_tokens", 0),
        output=usage.get("output_tokens", 0),
        thinking=(usage.get("output_tokens_details") or {}).get("thinking_tokens", 0),
        read=usage.get("cache_read_input_tokens", 0),
        write_5m=write_5m,
        write_1h=write_1h,
        web_searches=(usage.get("server_tool_use") or {}).get("web_search_requests", 0),
        responses=1,
    )


def add(target: ModelUsage, other: ModelUsage) -> None:
    for name in ("input", "output", "thinking", "read", "write_5m", "write_1h", "web_searches", "responses"):
        setattr(target, name, getattr(target, name) + getattr(other, name))


def tool_model_usage(usage: dict) -> ModelUsage:
    return ModelUsage(
        input=usage.get("inputTokens", 0),
        output=usage.get("outputTokens", 0),
        thinking=usage.get("thinkingTokens", 0),
        read=usage.get("cacheReadInputTokens", 0),
        write_5m=usage.get("cacheCreationInputTokens", 0),
        web_searches=usage.get("webSearchRequests", 0),
    )


def session_usage(paths: Iterable[Path]) -> SessionUsage:
    responses: dict[str, tuple[str, dict]] = {}
    tools: Counter[str] = Counter()
    tool_models: dict[str, dict] = {}
    for path in paths:
        for record in records(path.read_text(encoding="utf-8").splitlines()):
            if record.get("type") == "cost-state":
                tool_models.update(record.get("modelUsage") or {})
            if record.get("type") != "assistant":
                continue
            message = record.get("message") or {}
            responses[message["id"]] = (message.get("model", ""), message.get("usage") or {})
            for block in message.get("content") or []:
                if block.get("type") == "tool_use":
                    tools[block["name"]] += 1
    result = SessionUsage(tools=tools)
    for model, usage in responses.values():
        add(result.models.setdefault(model, ModelUsage()), response_usage(usage))
    for model, usage in tool_models.items():
        if model not in result.models:
            result.models[model] = tool_model_usage(usage)
    return result


def format_usd(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.0001'))} USD"


def render_usage(usage: SessionUsage, investors: int) -> str:
    lines = [
        f"Ceník: {PRICE_SOURCE} (otevřeno {PRICE_ACCESSED}), webové vyhledávání {WEB_SEARCH_USD} USD za dotaz.",
        "",
        "| Model | Odpovědí | Vstup | Výstup (z toho thinking) | Cache čtení | Cache zápis 5m | Cache zápis 1h | Vyhledávání | Tokenů celkem | Cena |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for model, item in sorted(usage.models.items()):
        lines.append(
            f"| {model} | {item.responses or '–'} | {item.input} | {item.output} ({item.thinking}) | {item.read} | {item.write_5m} | "
            f"{item.write_1h} | {item.web_searches} | {item.total} | {format_usd(item.cost(PRICES[model]))} |"
        )
    total_cost = usage.cost()
    lines += [
        "",
        f"Volání nástrojů: {', '.join(f'{name} {count}' for name, count in sorted(usage.tools.items()))}.",
        f"Celkem {usage.total_tokens} tokenů a {format_usd(total_cost)}.",
        f"Na investora (n = {investors}): {usage.total_tokens // investors} tokenů a {format_usd(total_cost / investors)}.",
    ]
    return "\n".join(lines) + "\n"
