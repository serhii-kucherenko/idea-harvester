# idea-harvester

Old, open, heavily-upvoted issues on commercial products' public trackers - where
traction and dissatisfaction are both already proven, and maintainers often state
why they won't fix it.

Repo-as-DB. `cards/` and `killed/` are the memory; the agent reads `killed/` each
run so past rejections become this run's negative examples.

## Run

1. `GH_TOKEN=` in `.env` (plain PAT, no scopes)
2. `python3 harvest.py > candidates.md` - deterministic, no LLM, cron-able
3. Open an agent session on `candidates.md` - it writes to `cards/` or `killed/`

Prefilter knobs live at the top of `harvest.py`: `MIN_REACTIONS`, `MIN_AGE_DAYS`.
Sources in `sources.json`.
