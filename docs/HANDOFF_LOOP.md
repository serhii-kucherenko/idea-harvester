# Harvest loop handoff

Paste into a fresh Agent chat in `idea-harvester`:

```
/loop 30m Read LOOP.md + CONTROLLER.json. Run one harvest tick (harvest.py, harvest_boards.py, harvest_discourse.py; score status:new; gc_cards.py; idle branch per LOOP). EMAIL RULE: Serhii wants ideas in his inbox, never outreach status. If >=24h since .email_digest_state.json last_ideas_email_at, run `python scripts/top_ideas_digest.py --ideas-email` and send it to kucherenko.web@gmail.com via Resend from "Serhii Ideas Bot <onboarding@resend.dev>", then `--mark-ideas-sent`. Never email outreach reminders. Promote new >=8 cards to eternal/ideas and mark promoted_eternal. Commit+push. Keep going; when context bloated, rewrite this handoff and open a fresh chat with this paste. Never start a second harvest loop — if CONTROLLER.loop.pid is alive, keep it and attach monitoring only. Prefer durable scripts/arm_harvest_sentinel.ps1 + watching .harvest_tick.log over ad-hoc Start-Sleep loops.
```

## Current state (2026-08-07 ~06:35 UTC)
- Live cards: 4 (all promoted to eternal/ideas), none new since 2026-07-26
- Email: **ideas digest only.** Latest: Resend `f118af9e-dbef-47d7-80de-504c14b9af90` (~06:35 UTC Aug 7) — collection sync focus; 8 screened / 0 shortlisted. Next after ~24h.
- Outreach reminders by email are **retired**. `OUTREACH.md` is the only place outreach state lives.
- Known problem: host trackers keep yielding core-host/pairwise kills. Source expansion beyond host trackers is the open question.
- Host PRs still open: Hoppscotch #5797, Supabase #42346
- Latest kills (tick 165): Fider #1211, Kong #14260, Harbor #12888, Gatus #638, Immich #4282/#5936, HA Sinope + Candy dishwasher
- Sentinel: pid **16212** via `scripts/arm_harvest_sentinel.ps1` — keep unless dead; attach by watching `.harvest_tick.log`
