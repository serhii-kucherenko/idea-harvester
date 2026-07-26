#!/usr/bin/env python3
"""Fetch old, open, heavily-upvoted issues from commercial products' public trackers.

No LLM. Numeric prefilter only - the agent scores survivors with RUBRIC.md.
Needs GH_TOKEN in .env (a plain GitHub PAT, no scopes needed for public repos).

Always emits up to TOP_N issues per repo (the shortlist). Already-judged URLs are
marked status: seen so the agent does not re-score them; only status: new is judged.

Mature repos use MIN_AGE_DAYS / MIN_REACTIONS. Repos listed in sources.json
young_repos use softer floors so newer products still fill a Top-5.

    python3 harvest.py > candidates.md
"""
import json, os, sys, urllib.request, urllib.parse, urllib.error, time
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


def search(repo, token, min_age_days):
    cutoff = (date.today() - timedelta(days=min_age_days)).isoformat()
    q = f"repo:{repo} is:issue is:open created:<{cutoff}"
    # pull a wider page then filter locally so TOP_N is reaction-true after min_reactions
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(
        {"q": q, "sort": "reactions", "order": "desc", "per_page": 30}
    )
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "idea-harvester",
    })
    # Search API is 30 req/min authed; one wait+retry on 403 rate limit.
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req) as r:
                return json.load(r)["items"]
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            if e.code == 403 and attempt == 0:
                time.sleep(65)
                continue
            print(f"# ERROR {repo}: HTTP {e.code} {body}", file=sys.stderr)
            return []
    return []


def top_n(issues, min_reactions):
    strong = [i for i in issues if i["reactions"]["total_count"] >= min_reactions]
    return strong[:TOP_N]


def main():
    load_env()
    token = os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("put GH_TOKEN=... in .env (plain GitHub PAT, no scopes needed for public repos)")
    seen = seen_urls()
    cfg = json.loads((HERE / "sources.json").read_text())
    repos = cfg["repos"]
    young = set(cfg.get("young_repos") or [])
    young_age = int(cfg.get("young_min_age_days", 120))
    young_rx = int(cfg.get("young_min_reactions", 8))

    print(f"# candidates {date.today()}")
    print(f"# top {TOP_N} per repo | mature: +1s>={MIN_REACTIONS} age>={MIN_AGE_DAYS}d"
          f" | young: +1s>={young_rx} age>={young_age}d")
    print(f"# score new items with RUBRIC.md; ignore status: seen\n")
    new_count = 0
    for repo in repos:
        is_young = repo in young
        age = young_age if is_young else MIN_AGE_DAYS
        rx = young_rx if is_young else MIN_REACTIONS
        tier = "young" if is_young else "mature"
        shortlist = top_n(search(repo, token, age), rx)
        time.sleep(2.1)  # search API ~30/min authed; keep headroom
        print(f"# {repo} ({len(shortlist)}/{TOP_N}) [{tier}]")
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
    got = top_n(issues, MIN_REACTIONS)
    assert [x["html_url"] for x in got] == ["a", "b", "c", "d", "e"]
    assert len(top_n(issues, 8)) == 5
    print("ok")


if __name__ == "__main__":
    selftest() if "--selftest" in sys.argv else main()
