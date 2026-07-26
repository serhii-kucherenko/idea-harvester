#!/usr/bin/env python3
"""Fetch old, open, heavily-upvoted issues from commercial products' public trackers.

No LLM. Numeric prefilter only - the agent scores survivors with RUBRIC.md.
Needs GH_TOKEN in .env (a plain GitHub PAT, no scopes needed for public repos).

Always emits up to TOP_N issues per repo (the shortlist). Already-judged URLs are
marked status: seen so the agent does not re-score them; only status: new is judged.

    python3 harvest.py > candidates.md
"""
import json, os, sys, urllib.request, urllib.parse
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent
MIN_REACTIONS = 15
MIN_AGE_DAYS = 540  # ~18mo unaddressed is the "they won't fix it" tell
TOP_N = 5  # always shortlist top 5 per source


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
    # pull a wider page then filter locally so TOP_N is reaction-true after MIN_REACTIONS
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(
        {"q": q, "sort": "reactions", "order": "desc", "per_page": 30}
    )
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "idea-harvester",
    })
    # ponytail: no retry/backoff. Search API is 30 req/min authed; add backoff if you exceed it.
    with urllib.request.urlopen(req) as r:
        return json.load(r)["items"]


def top_n(issues):
    strong = [i for i in issues if i["reactions"]["total_count"] >= MIN_REACTIONS]
    return strong[:TOP_N]


def main():
    load_env()
    token = os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("put GH_TOKEN=... in .env (plain GitHub PAT, no scopes needed for public repos)")
    seen = seen_urls()
    repos = json.loads((HERE / "sources.json").read_text())["repos"]
    print(f"# candidates {date.today()}")
    print(f"# top {TOP_N} per repo, min +1s={MIN_REACTIONS}, age>={MIN_AGE_DAYS}d")
    print(f"# score new items with RUBRIC.md; ignore status: seen\n")
    new_count = 0
    for repo in repos:
        shortlist = top_n(search(repo, token))
        print(f"# {repo} ({len(shortlist)}/{TOP_N})")
        if not shortlist:
            print(f"# (no issues met filters)\n")
            continue
        for i in shortlist:
            url = i["html_url"]
            status = "seen" if url in seen else "new"
            if status == "new":
                new_count += 1
            print(f"## {i['title']}")
            print(f"source: {url}")
            print(f"status: {status}")
            print(f"repo: {repo} | +1s: {i['reactions']['total_count']} "
                  f"| comments: {i['comments']} | opened: {i['created_at'][:10]}\n")
            if status == "new":
                print((i["body"] or "")[:400].strip() + "\n")
        print()
    print(f"# summary: {new_count} new to judge")


def selftest():
    issues = [
        {"html_url": "a", "reactions": {"total_count": 100}},
        {"html_url": "b", "reactions": {"total_count": 50}},
        {"html_url": "c", "reactions": {"total_count": 20}},
        {"html_url": "d", "reactions": {"total_count": 18}},
        {"html_url": "e", "reactions": {"total_count": 16}},
        {"html_url": "f", "reactions": {"total_count": 14}},
        {"html_url": "g", "reactions": {"total_count": 90}},
    ]
    got = top_n(issues)
    assert [x["html_url"] for x in got] == ["a", "b", "c", "d", "e"]
    assert all(x["reactions"]["total_count"] >= MIN_REACTIONS for x in got)
    print("ok")


if __name__ == "__main__":
    selftest() if "--selftest" in sys.argv else main()
