# Keep-going harvest loop

Borrowed from ai-method-lab's endless keep-executing loop — **loop mechanics only**
(no product studios, papers intake, or email).

## One tick

1. Read `CONTROLLER.json`. If `mode` is `paused` or `hard_stop`, stop.
2. `python3 harvest.py > candidates.md` and `python3 harvest_boards.py > candidates_boards.md`
3. Score every `status: new` item with `RUBRIC.md` (≥8 → `cards/`, else `killed/`).
4. `python3 gc_cards.py`
5. **Idle branch** (0 new, or 0 live cards after GC): improve the machine —
   - expand `sources.json` (new repos and/or public boards)
   - sharpen `RUBRIC.md` if a new fail pattern appeared
   - optionally retune `MIN_REACTIONS` / `MIN_AGE_DAYS` for young products
   - re-harvest once in the same tick if sources changed
6. Commit (message: what this tick learned or carded), then `git push origin HEAD`. Do not ask the human.
7. Re-arm the loop sentinel. Stop only on human stop or `hard_stop`.

## Rules

- No confirmation between ticks
- Pain quote ≠ company; solo gate stays strict
- Always Top 5 shortlist per source
- `killed/` is permanent negative memory
- Prefer live cards that a one-founder SaaS could ship in weeks

## Sentinel

`AGENT_LOOP_TICK_harvest` — interval in `CONTROLLER.json` → `loop.interval`
