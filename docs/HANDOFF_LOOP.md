# Harvest loop handoff

Paste into a fresh Agent chat in `idea-harvester`:

```
/loop 30m Read LOOP.md + CONTROLLER.json + OUTREACH.md. Run one harvest tick (harvest.py, harvest_boards.py, harvest_discourse.py; score status:new; gc_cards.py; idle branch per LOOP). Check top_ideas_digest.py — if unsent_top_cards>0 email digest to kucherenko.web@gmail.com via Resend from "Serhii Ideas Bot <onboarding@resend.dev>", then --mark-current-sent. Do NOT auto-blast design-partner leads; if OUTREACH still unsent, email Serhii a short reminder with the ready drafts (from onboarding@resend.dev, at most once per 6h). Promote new >=8 cards to eternal/ideas and mark promoted_eternal. Commit+push. Keep going; when context bloated, rewrite this handoff and open a fresh chat with this paste. Never start a second harvest loop — if CONTROLLER.loop.pid is alive, keep it and attach monitoring only by replacing it once in the new chat.
```

## Current state (2026-07-31)
- Live cards: 4 (all promoted to eternal/ideas)
- Digests: all 4 already sent to kucherenko.web@gmail.com
- OUTREACH: 4 emails + Aaron LinkedIn still unsent from personal inbox
- Reminder emailed to Serhii: Resend id b2c29685-97b8-40c9-868e-7f0c3373852c (skip re-send until ~18:30 UTC)
- Latest kill: Twenty #7296 WhatsApp Business sync (pairwise); prior Sentry #84596
- Sentinel: pid 34140 in CONTROLLER.json (tick 71) — keep unless dead
- Prefer skip host expand while consecutive_all_kill_expands >= 3 and OUTREACH ready
- Why handoff: this chat context is bloating after repeated idle ticks
