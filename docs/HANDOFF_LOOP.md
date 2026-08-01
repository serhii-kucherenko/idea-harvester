# Harvest loop handoff

Paste into a fresh Agent chat in `idea-harvester`:

```
/loop 30m Read LOOP.md + CONTROLLER.json + OUTREACH.md. Run one harvest tick (harvest.py, harvest_boards.py, harvest_discourse.py; score status:new; gc_cards.py; idle branch per LOOP). Check top_ideas_digest.py — if unsent_top_cards>0 email digest to kucherenko.web@gmail.com via Resend from "Serhii Ideas Bot <onboarding@resend.dev>", then --mark-current-sent. Do NOT auto-blast design-partner leads; if OUTREACH still unsent, email Serhii a short reminder with the ready drafts (from onboarding@resend.dev, at most once per 6h). Promote new >=8 cards to eternal/ideas and mark promoted_eternal. Commit+push. Keep going; when context bloated, rewrite this handoff and open a fresh chat with this paste. Never start a second harvest loop — if CONTROLLER.loop.pid is alive, keep it and attach monitoring only by replacing it once in the new chat.
```

## Current state (2026-08-01 ~05:38 UTC)
- Live cards: 4 (all promoted to eternal/ideas)
- Digests: all sent (`unsent_top_cards: 0`)
- OUTREACH: 5 drafts still unsent from personal inbox
- Latest outreach reminder: Resend `367ecfec-6599-45bf-be64-0dd52f78d12b` (~04:27 UTC Aug 1) — next after ~10:27 UTC Aug 1
- Host PRs still open: Hoppscotch #5797, Supabase #42346
- Sentinel: pid **10428** (tick 105) — keep unless dead; kill any other `AGENT_LOOP_TICK_harvest` PowerShell
- Prefer skip host expand while consecutive_all_kill_expands >= 3 and OUTREACH ready
- Context bloated: prefer fresh chat with the paste above; do not start a second loop
