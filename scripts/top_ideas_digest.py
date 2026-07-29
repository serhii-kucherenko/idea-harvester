#!/usr/bin/env python3
"""Build and dedupe email digest payloads for top idea cards.

Usage:
  python scripts/top_ideas_digest.py
  python scripts/top_ideas_digest.py --mark-current-sent
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = ROOT / "cards"
STATE_PATH = ROOT / ".email_digest_state.json"
TOP_N = 5


def _parse_card(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    title = path.stem
    source = ""
    score = -1
    one_liner = ""
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("source:"):
            source = line.split(":", 1)[1].strip()
        elif line.startswith("score:"):
            raw = line.split(":", 1)[1].strip()
            score = int(raw.split("/", 1)[0].strip())
        elif line.startswith("## Product angle"):
            one_liner = "Product angle available in card."

    if not source:
        return {}
    return {
        "title": title,
        "source": source,
        "score": score,
        "card_path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "summary": one_liner or "See card for details.",
    }


def _load_state() -> dict:
    if not STATE_PATH.exists():
        return {"sent_sources": [], "updated_at": None}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def _save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def _load_top_cards() -> list[dict]:
    cards = []
    for path in CARDS_DIR.glob("*.md"):
        if path.name == ".gitkeep":
            continue
        card = _parse_card(path)
        if card:
            cards.append(card)
    cards.sort(key=lambda c: c["score"], reverse=True)
    return cards[:TOP_N]


def compute_payload() -> dict:
    state = _load_state()
    top_cards = _load_top_cards()
    sent_sources = set(state.get("sent_sources", []))
    unsent_top_cards = [c for c in top_cards if c["source"] not in sent_sources]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "top_cards": top_cards,
        "unsent_top_cards": unsent_top_cards,
        "sent_count": len(sent_sources),
        "state_path": str(STATE_PATH),
    }


def mark_current_top_sent() -> dict:
    payload = compute_payload()
    state = _load_state()
    sent_sources = set(state.get("sent_sources", []))
    for card in payload["unsent_top_cards"]:
        sent_sources.add(card["source"])
    state["sent_sources"] = sorted(sent_sources)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_state(state)
    return compute_payload()


def main() -> None:
    import sys

    if "--mark-current-sent" in sys.argv:
        result = mark_current_top_sent()
    else:
        result = compute_payload()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
