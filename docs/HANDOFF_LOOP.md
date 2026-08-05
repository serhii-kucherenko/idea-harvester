# Harvest loop handoff

Paste into a fresh Agent chat in `idea-harvester`:

```
/loop 30m Read LOOP.md + CONTROLLER.json. Run one harvest tick (harvest.py, harvest_boards.py, harvest_discourse.py; score status:new; gc_cards.py; idle branch per LOOP). EMAIL RULE: Serhii wants ideas in his inbox, never outreach status. If >=24h since .email_digest_state.json last_ideas_email_at, run `python scripts/top_ideas_digest.py --ideas-email` and send it to kucherenko.web@gmail.com via Resend from "Serhii Ideas Bot <onboarding@resend.dev>", then `--mark-ideas-sent`. Never email outreach reminders. Promote new >=8 cards to eternal/ideas and mark promoted_eternal. Commit+push. Keep going; when context bloated, rewrite this handoff and open a fresh chat with this paste. Never start a second harvest loop — if CONTROLLER.loop.pid is alive, keep it and attach monitoring only. Prefer durable scripts/arm_harvest_sentinel.ps1 + watching .harvest_tick.log over ad-hoc Start-Sleep loops.
```

## Current state (2026-08-05 ~07:40 UTC)
- Live cards: 4 (all promoted to eternal/ideas), none new since 2026-07-26
- Email: **ideas digest only.** `scripts/top_ideas_digest.py --ideas-email` always has content —
  it rotates which live idea gets the deep write-up and reports what was screened and rejected
  since the last send. First one sent Aug 5 (Resend `6e900936-ca59-4509-a33b-9d9a041379c5`).
- Outreach reminders by email are **retired**. Serhii asked for ideas, not outreach status.
  `OUTREACH.md` is the only place outreach state lives.
- Known problem: ~780 candidates screened since the last email, 0 shortlisted. Host issue
  trackers mostly surface work the host should do itself, so the funnel is starving.
  Source expansion beyond host trackers is the open question.
- Host PRs still open: Hoppscotch #5797, Supabase #42346
- Sentinel: pid **16212** via `scripts/arm_harvest_sentinel.ps1` — keep unless dead; attach by
  watching `.harvest_tick.log`
