import json
import re
from typing import Any


def _strip_markdown_fences(text: str) -> str:
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()


def _parse_with_decoder(text: str) -> Any | None:
    decoder = json.JSONDecoder()
    idx = text.find("{")
    if idx < 0:
        return None
    try:
        return decoder.raw_decode(text, idx)[0]
    except json.JSONDecodeError:
        return None


def _regex_json_object(text: str) -> Any | None:
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None
    blob = match.group(0)
    try:
        return json.loads(blob)
    except json.JSONDecodeError:
        return None


def parse_ui_actions_response(raw: str) -> dict[str, Any]:
    if not raw or not raw.strip():
        return {"actions": []}

    text = raw.strip()

    for candidate in (text, _strip_markdown_fences(text)):
        if not candidate:
            continue
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    for candidate in (_parse_with_decoder(text), _parse_with_decoder(_strip_markdown_fences(text))):
        if candidate is not None:
            return candidate

    fallback = _regex_json_object(text)
    if fallback is not None:
        return fallback

    return {"actions": []}


def normalize_actions_payload(parsed: Any) -> dict[str, Any]:
    if not isinstance(parsed, dict):
        return {"actions": []}
    if "actions" not in parsed:
        return {"actions": []}
    actions = parsed.get("actions")
    if not isinstance(actions, list):
        return {"actions": []}
    out: list[dict[str, Any]] = []
    for item in actions:
        if not isinstance(item, dict):
            continue
        if item.get("function") != "applyStyle":
            continue
        params = item.get("params")
        if not isinstance(params, dict):
            continue
        selector = params.get("selector")
        styles = params.get("styles")
        if not isinstance(selector, str) or not isinstance(styles, dict):
            continue
        out.append(
            {
                "function": "applyStyle",
                "params": {"selector": selector, "styles": styles},
            }
        )
    return {"actions": out}
