#!/usr/bin/env python3
"""Self-garbage-collect live cards against RUBRIC.md rules. No LLM.

    python3 gc_cards.py          # apply moves
    python3 gc_cards.py --dry-run
"""
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).parent
CARDS = HERE / "cards"
KILLED = HERE / "killed"
MAX_CARDS = 15
STALE_DAYS = 45


def parse_card(path: Path):
    text = path.read_text()
    meta = {"path": path, "title": path.stem, "score": None, "scored": None, "source": None}
    for line in text.splitlines():
        if line.startswith("# "):
            meta["title"] = line[2:].strip()
        elif line.startswith("source:"):
            meta["source"] = line.split(None, 1)[1].strip()
        elif line.startswith("score:"):
            m = re.search(r"(\d+)\s*/\s*10", line)
            meta["score"] = int(m.group(1)) if m else None
        elif line.startswith("scored:"):
            raw = line.split(None, 1)[1].strip()
            try:
                meta["scored"] = date.fromisoformat(raw)
            except ValueError:
                meta["scored"] = None
    return meta, text


def kill(path: Path, text: str, reason: str, dry: bool):
    lines = text.splitlines()
    out = []
    replaced = False
    for line in lines:
        if line.startswith("killed:"):
            out.append(f"killed: {reason}")
            replaced = True
        elif line.startswith("score:") or line.startswith("dimensions:") or line.startswith("scored:"):
            continue
        else:
            out.append(line)
    if not replaced:
        # insert after source:
        final = []
        inserted = False
        for line in out:
            final.append(line)
            if line.startswith("source:") and not inserted:
                final.append(f"killed: {reason}")
                inserted = True
        if not inserted:
            final.extend(["", f"killed: {reason}"])
        out = final
    dest = KILLED / path.name
    if dry:
        print(f"DRY kill {path.name} -> {reason}")
        return
    dest.write_text("\n".join(out).rstrip() + "\n")
    path.unlink()
    print(f"kill {path.name} -> {reason}")


def main():
    dry = "--dry-run" in sys.argv
    cards = sorted(CARDS.glob("*.md"))
    if not cards:
        print("no live cards")
        return

    parsed = [parse_card(p) for p in cards]
    today = date.today()
    stale_before = today - timedelta(days=STALE_DAYS)

    survivors = []
    for meta, text in parsed:
        if meta["score"] is None or meta["score"] < 8:
            kill(meta["path"], text, "below-rubric", dry)
            continue
        if meta["scored"] is None or meta["scored"] < stale_before:
            kill(meta["path"], text, "stale", dry)
            continue
        survivors.append((meta, text))

    # highest score first, then newest scored
    survivors.sort(
        key=lambda pair: (pair[0]["score"] or 0, pair[0]["scored"] or date.min),
        reverse=True,
    )

    for meta, text in survivors[MAX_CARDS:]:
        kill(meta["path"], text, "gc-cap", dry)

    kept = min(len(survivors), MAX_CARDS)
    print(f"kept={kept} cap={MAX_CARDS}")


def selftest():
    sample = "# T\nsource: https://x\nscore: 9/10\nscored: 2026-07-01\n"
    p = HERE / ".gc_selftest.md"
    p.write_text(sample)
    meta, _ = parse_card(p)
    assert meta["score"] == 9 and meta["scored"] == date(2026, 7, 1)
    p.unlink()
    print("ok")


if __name__ == "__main__":
    selftest() if "--selftest" in sys.argv else main()
