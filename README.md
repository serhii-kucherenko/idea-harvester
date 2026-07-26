# idea-harvester

Find solo-indie product wedges from old, open, heavily-upvoted tracker issues -
where demand is proven and maintainers often say why they will not fix it.

Repo-as-DB. `cards/` and `killed/` are the memory. Read `RUBRIC.md` before judging.
`killed/` entries are negative examples for later runs.

## Run

1. `GH_TOKEN=` in `.env` (plain PAT, no scopes)
2. `python3 harvest.py > candidates.md` - top 5 issues per source, marks `new` vs `seen`
3. `python3 harvest_boards.py > candidates_boards.md` - top 5 GitHub Discussions Ideas
4. Agent scores every `status: new` item with `RUBRIC.md` → `cards/` or `killed/`
5. `python3 gc_cards.py` - enforce score floor, 45-day stale, 15-card cap

Keep-going autonomous loop: `LOOP.md` + `CONTROLLER.json` (ai-method-lab endless-loop mechanics only).

## Rules of thumb

- Pain quote ≠ company. Card only solo-shippable monthly products (≥8/10).
- Always shortlist top 5 per source; do not collapse a source to zero before scoring.
- Hard-fail integrations, host drivers/plugins, and core host UI/engine work.

Prefilter knobs: `TOP_N`, `MIN_REACTIONS`, `MIN_AGE_DAYS` in `harvest.py`.
Sources: `sources.json` (GitHub repos now; boards listed for the next connector).
