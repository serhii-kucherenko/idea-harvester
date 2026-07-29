#!/usr/bin/env python3
"""Build and dedupe email digest payloads for top idea cards.

Usage:
  python scripts/top_ideas_digest.py
  python scripts/top_ideas_digest.py --mark-current-sent
"""
from __future__ import annotations

import json
import re
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
    repo = ""
    dimensions = ""
    sections: dict[str, str] = {}
    current_section = ""
    section_lines: list[str] = []

    def flush_section() -> None:
        if current_section:
            sections[current_section] = "\n".join(section_lines).strip()

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("source:"):
            source = line.split(":", 1)[1].strip()
        elif line.startswith("repo:"):
            repo = line.split(":", 1)[1].strip()
        elif line.startswith("score:"):
            raw = line.split(":", 1)[1].strip()
            score = int(raw.split("/", 1)[0].strip())
        elif line.startswith("dimensions:"):
            dimensions = line.split(":", 1)[1].strip()
        elif line.startswith("## "):
            flush_section()
            current_section = line[3:].strip().lower()
            section_lines = []
        elif line.startswith("## Product angle"):
            continue
        elif current_section:
            section_lines.append(line)

    flush_section()

    if not source:
        return {}
    decision = "PURSUE"
    if score < 8:
        decision = "HOLD"
    if "host-risk=1" in dimensions:
        decision = "PURSUE (time-boxed)"

    return {
        "title": title,
        "source": source,
        "score": score,
        "repo": repo,
        "dimensions": dimensions,
        "card_path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "gap": sections.get("gap", "Not captured."),
        "why_host_wont": sections.get("why host won't", "Not captured."),
        "product_angle": sections.get("product angle", "Not captured."),
        "competition": sections.get("competition / workarounds", "Not captured."),
        "kill_if": sections.get("kill if", "Not captured."),
        "tick_note": sections.get("tick note", ""),
        "decision": decision,
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


def _dimensions_to_summary(dimensions: str) -> str:
    if not dimensions:
        return "No dimension breakdown."
    pairs = re.findall(r"([a-z-]+)=(\d+)", dimensions)
    if not pairs:
        return dimensions
    label_map = {
        "standalone": "standalone",
        "wtp": "willingness-to-pay",
        "host-risk": "host-displacement risk",
        "solo-ship": "solo-shippability",
        "distribution": "distribution ease",
    }
    chunks = []
    for key, value in pairs:
        name = label_map.get(key, key)
        chunks.append(f"{name}: {value}/2")
    return ", ".join(chunks)


def render_email_text(cards: list[dict], generated_at: str) -> str:
    lines: list[str] = []
    lines.append("Idea Harvester - Decision Brief")
    lines.append("")
    lines.append(
        "This digest is designed to help you decide what to pursue, not just list ideas."
    )
    lines.append(f"Generated: {generated_at}")
    lines.append("")
    for idx, card in enumerate(cards, start=1):
        lines.append(f"{idx}) {card['title']} ({card['score']}/10) - {card['decision']}")
        lines.append(f"Repo signal: {card.get('repo') or 'n/a'}")
        lines.append(f"Source: {card['source']}")
        lines.append(f"What it is: {card['gap']}")
        lines.append(f"Why this can exist now: {card['why_host_wont']}")
        lines.append(f"How you'd build/sell first: {card['product_angle']}")
        lines.append(f"Competition/workarounds: {card['competition']}")
        lines.append(f"What would kill it: {card['kill_if']}")
        lines.append(
            f"Rubric breakdown: {_dimensions_to_summary(card.get('dimensions', ''))}"
        )
        if card.get("tick_note"):
            lines.append(f"Latest revalidation note: {card['tick_note']}")
        lines.append("")

    lines.append("How to use this:")
    lines.append("- Pick 1 idea only.")
    lines.append("- Run 3 design-partner calls in 7 days.")
    lines.append("- If fewer than 3 strong yeses, move to the next idea.")
    return "\n".join(lines)


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
    elif "--email-text" in sys.argv:
        payload = compute_payload()
        only_unsent = "--unsent-only" in sys.argv
        cards = payload["unsent_top_cards"] if only_unsent else payload["top_cards"]
        print(render_email_text(cards, payload["generated_at"]))
        return
    else:
        result = compute_payload()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
