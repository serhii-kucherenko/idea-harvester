#!/usr/bin/env python3
"""Harvest old, highly-liked topics from public Discourse feature boards.

Complements harvest.py / harvest_boards.py. Same memory (cards/killed source: URLs).

    python3 harvest_discourse.py > candidates_discourse.md
"""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
TOP_N = 5
MIN_LIKES = 10
MIN_AGE_DAYS = 180
UA = {"User-Agent": "idea-harvester"}


def seen_urls() -> set[str]:
    return {
        line.split()[-1]
        for d in ("cards", "killed")
        for f in (HERE / d).glob("*.md")
        for line in f.read_text(encoding="utf-8").splitlines()
        if line.startswith("source:")
    }


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch_board(board: dict) -> list[dict]:
    base = board["base_url"].rstrip("/")
    path = board["category_path"].lstrip("/")
    url = f"{base}/{path}.json"
    data = fetch_json(url)
    topics = (data.get("topic_list") or {}).get("topics") or []
    cutoff = datetime.now(timezone.utc) - timedelta(
        days=board.get("min_age_days", MIN_AGE_DAYS)
    )
    min_likes = board.get("min_likes", MIN_LIKES)
    kept: list[dict] = []
    for t in topics:
        title = t.get("title") or ""
        if t.get("pinned") or title.startswith("About the "):
            continue
        created_raw = t.get("created_at") or ""
        created = datetime.fromisoformat(created_raw.replace("Z", "+00:00"))
        if created > cutoff:
            continue
        likes = t.get("like_count") or 0
        if likes < min_likes:
            continue
        slug = t.get("slug") or "topic"
        tid = t.get("id")
        kept.append(
            {
                "title": title,
                "url": f"{base}/t/{slug}/{tid}",
                "likes": likes,
                "posts": t.get("posts_count") or 0,
                "created": created_raw[:10],
                "category": board.get("name") or path,
            }
        )
    kept.sort(key=lambda n: n["likes"], reverse=True)
    return kept[: board.get("top_n", TOP_N)]


def main() -> None:
    cfg = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))
    boards = cfg.get("discourse_boards") or []
    if not boards:
        sys.exit("no discourse_boards in sources.json")
    seen = seen_urls()
    print(f"# discourse candidates {date.today()}")
    print(f"# Top {TOP_N}, min likes={MIN_LIKES}, age>={MIN_AGE_DAYS}d\n")
    new_count = 0
    for board in boards:
        label = board.get("name") or board.get("base_url")
        try:
            items = fetch_board(board)
        except Exception as e:
            print(f"# ERROR {label}: {e}", file=sys.stderr)
            print(f"# {label} (0/{TOP_N}) [error]\n")
            continue
        print(f"# {label} ({len(items)}/{TOP_N}) [discourse]")
        if not items:
            print("# (no topics met filters)\n")
            continue
        for n in items:
            status = "seen" if n["url"] in seen else "new"
            if status == "new":
                new_count += 1
            print(f"## {n['title']}")
            print(f"source: {n['url']}")
            print(f"status: {status}")
            print(
                f"board: {n['category']} | likes: {n['likes']} "
                f"| posts: {n['posts']} | opened: {n['created']}\n"
            )
        print()
    print(f"# summary: {new_count} new to judge")


if __name__ == "__main__":
    main()
