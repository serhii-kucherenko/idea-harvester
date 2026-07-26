#!/usr/bin/env python3
"""Harvest old, open, highly-upvoted GitHub Discussions (Ideas boards).

Complements harvest.py issue search. Same memory (cards/killed source: URLs).
Needs GH_TOKEN in .env.

    python3 harvest_boards.py > candidates_boards.md
"""
import json, os, sys, urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
TOP_N = 5
MIN_UPVOTES = 15
MIN_AGE_DAYS = 180


def load_env():
    for line in (HERE / ".env").read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def seen_urls():
    return {
        line.split()[-1]
        for d in ("cards", "killed")
        for f in (HERE / d).glob("*.md")
        for line in f.read_text().splitlines()
        if line.startswith("source:")
    }


def gql(token, query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "idea-harvester",
        },
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]


SEARCH = """
query($q: String!) {
  search(query: $q, type: DISCUSSION, first: 30) {
    nodes {
      ... on Discussion {
        title
        url
        createdAt
        upvoteCount
        comments { totalCount }
        category { name }
        repository { nameWithOwner }
      }
    }
  }
}
"""


def fetch_board(token, board):
    # board: {repo, query_extra?}
    repo = board["repo"]
    extra = board.get("query_extra", "")
    q = f"repo:{repo} is:open {extra}".strip()
    data = gql(token, SEARCH, {"q": q})
    nodes = [n for n in data["search"]["nodes"] if n]
    cutoff = datetime.now(timezone.utc) - timedelta(days=board.get("min_age_days", MIN_AGE_DAYS))
    min_up = board.get("min_upvotes", MIN_UPVOTES)
    kept = []
    for n in nodes:
        created = datetime.fromisoformat(n["createdAt"].replace("Z", "+00:00"))
        if created > cutoff:
            continue
        if (n.get("upvoteCount") or 0) < min_up:
            continue
        kept.append(n)
    kept.sort(key=lambda n: n.get("upvoteCount") or 0, reverse=True)
    return kept[: board.get("top_n", TOP_N)]


def main():
    load_env()
    token = os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("put GH_TOKEN=... in .env")
    cfg = json.loads((HERE / "sources.json").read_text())
    boards = cfg.get("discussion_boards") or []
    if not boards:
        sys.exit("no discussion_boards in sources.json")
    seen = seen_urls()
    print(f"# board candidates {date.today()}")
    print(f"# GitHub Discussions top {TOP_N}, min upvotes={MIN_UPVOTES}, age>={MIN_AGE_DAYS}d\n")
    new_count = 0
    for board in boards:
        repo = board["repo"]
        try:
            items = fetch_board(token, board)
        except Exception as e:
            print(f"# ERROR {repo}: {e}", file=sys.stderr)
            print(f"# {repo} (0/{TOP_N}) [error]\n")
            continue
        print(f"# {repo} ({len(items)}/{TOP_N}) [discussions]")
        if not items:
            print("# (no discussions met filters)\n")
            continue
        for n in items:
            url = n["url"]
            status = "seen" if url in seen else "new"
            if status == "new":
                new_count += 1
            print(f"## {n['title']}")
            print(f"source: {url}")
            print(f"status: {status}")
            cat = (n.get("category") or {}).get("name") or "?"
            print(
                f"repo: {n['repository']['nameWithOwner']} | upvotes: {n['upvoteCount']} "
                f"| comments: {n['comments']['totalCount']} | opened: {n['createdAt'][:10]} "
                f"| category: {cat}\n"
            )
        print()
    print(f"# summary: {new_count} new to judge")


def selftest():
    assert TOP_N == 5 and MIN_UPVOTES >= 1
    print("ok")


if __name__ == "__main__":
    selftest() if "--selftest" in sys.argv else main()
