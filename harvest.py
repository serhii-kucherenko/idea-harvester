#!/usr/bin/env python3
"""Fetch old, open, heavily-upvoted issues from commercial products' public trackers.

No LLM. Numeric prefilter only - the agent does the judgment on the survivors.
Needs GH_TOKEN in .env (a plain GitHub PAT, no scopes needed for public repos).

    python3 harvest.py > candidates.md
"""
import json, os, sys, urllib.request, urllib.parse
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent
MIN_REACTIONS = 15
MIN_AGE_DAYS = 540  # ~18mo unaddressed is the "they won't fix it" tell
PER_REPO = 10


def load_env():
    # ponytail: no quote stripping or multiline values. Add if a secret ever needs them.
    for line in (HERE / ".env").read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def seen_urls():
    """Every issue already judged - card or kill. Dedupe is the whole memory."""
    return {
        line.split()[-1]
        for d in ("cards", "killed")
        for f in (HERE / d).glob("*.md")
        for line in f.read_text().splitlines()
        if line.startswith("source:")
    }


def search(repo, token):
    cutoff = (date.today() - timedelta(days=MIN_AGE_DAYS)).isoformat()
    q = f"repo:{repo} is:issue is:open created:<{cutoff}"
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(
        {"q": q, "sort": "reactions", "order": "desc", "per_page": PER_REPO}
    )
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "idea-harvester",
    })
    # ponytail: no retry/backoff. Search API is 30 req/min authed; add backoff if you exceed it.
    with urllib.request.urlopen(req) as r:
        return json.load(r)["items"]


def keep(issue, seen):
    return (
        issue["html_url"] not in seen
        and issue["reactions"]["total_count"] >= MIN_REACTIONS
    )


def main():
    load_env()
    token = os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("put GH_TOKEN=... in .env (plain GitHub PAT, no scopes needed for public repos)")
    seen = seen_urls()
    repos = json.loads((HERE / "sources.json").read_text())["repos"]
    print(f"# candidates {date.today()}\n")
    for repo in repos:
        for i in search(repo, token):
            if not keep(i, seen):
                continue
            print(f"## {i['title']}")
            print(f"source: {i['html_url']}")
            print(f"repo: {repo} | +1s: {i['reactions']['total_count']} "
                  f"| comments: {i['comments']} | opened: {i['created_at'][:10]}\n")
            print((i["body"] or "")[:400].strip() + "\n")


def selftest():
    old = {"html_url": "u", "reactions": {"total_count": 20}}
    assert keep(old, set())
    assert not keep(old, {"u"}), "dedupe failed"
    assert not keep({"html_url": "v", "reactions": {"total_count": 2}}, set())
    print("ok")


if __name__ == "__main__":
    selftest() if "--selftest" in sys.argv else main()
