# Live cards scorecard

Solo-indie gate (RUBRIC.md). Revalidated each idle tick when intake is empty.

| Card | Score | One-liner | Concierge in a week? | Main risk |
|------|------:|-----------|----------------------|-----------|
| [API collection git sync](cards/hoppscotch-870-feature-sync-collections-with-git-r.md) | 8/10 | Git sync for Hoppscotch/Postman/Insomnia collections | Yes - CLI + GitHub App | Hosts ship native git sync (draft PR #5797) |
| [RLS debugger](cards/supabase-12269-add-feature-to-test-debug-row-level.md) | 8/10 | Test Postgres RLS policies against sample JWTs | Yes - SQL harness + UI | Supabase ships it |
| [DMARC reports](cards/mailcow-dockerized-1341-feature-request-dmarc-report-parser.md) | 8/10 | Cheap DMARC dashboard for self-hosted mail | Yes - parse rua mailbox | Enterprise DMARC suites / Mailcow UI |
| [Coolify backups](cards/coolify-2389-feature-backup-manger-in-the-ui.md) | 8/10 | Scheduled backups/restore for self-hosted PaaS | Yes - S3 + restore drills | Coolify ships good enough backups |

**Pick order for validation:** collection sync → RLS → DMARC → Coolify backups.

**Idle note (2026-07-30x):** 0 new. Skipped expand. Host PRs still open. Deduped sentinel (kept 19768, stopped 31516). Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30w):** 0 new. Skipped expand. Host PRs still open. Deduped sentinel (kept 19768, stopped 31828). Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30v):** 0 new. Skipped expand. Host PRs still open. Deduped sentinel (kept 19768, stopped 25344). Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30u):** 0 new. Skipped expand. Host PRs still open. Deduped sentinel (kept 19768, stopped 27124). Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30t):** 0 new. Skipped expand. Host PRs still open. Deduped sentinel (kept 19768, stopped 21268). Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30s):** 0 new. Skipped expand. Host PRs still open. Deduped again (stopped pid 33004; keep 31440). Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30r):** 0 new. Skipped expand. Host PRs still open. Deduped harvest sentinels to pid 31440. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30q):** 0 new. Skipped expand. Host PRs still open. Eternal promotions already marked. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30p):** 0 new. Skipped expand. Revalidated all 4 live sources + PRs #5797/#42346 — still open. Promoted all 4 cards into eternal/ideas and marked `promoted_eternal` on each card. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30o):** 0 new. Skipped expand. Host PRs still open. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30n):** 1 board new (Immich .nomedia/.immichignore) → core-host kill. Skipped expand. Host PRs still open. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30m):** 0 new. Skipped expand. Host PRs still open. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30l):** 0 new. Skipped expand. Host PRs still open. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30k):** 0 new. Skipped expand. Host PRs still open. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30j):** 1 board new (Immich WebDAV) → host-driver kill. Skipped expand. Host PRs still open. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30i):** 0 new. Skipped expand. Host PRs still open. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30h):** 1 board new (Immich thumbnail icons) → core-host kill. Skipped expand. Host PRs still open. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30g):** 0 new. Skipped expand. Host PRs still open. Still blocked on OUTREACH personal sends.

**Idle note (2026-07-30f):** 0 new. Skipped expand. Host PRs still open. OUTREACH checklist unchanged — still blocked on personal send.

**Idle note (2026-07-30e):** 0 new. Skipped expand again. Host PRs #5797/#42346 still open/unmerged. No public email for @munaf-khatri. OUTREACH checklist unchanged — personal send still the only high-leverage move.

**Idle note (2026-07-30d):** 0 new. Skipped host expand (4 consecutive all-kill expands; LOOP outreach preference). Revalidated all 4 live sources + PRs #5797/#42346 — still open. Added OUTREACH send checklist. Human send remains the blocker.

**Idle note (2026-07-30c):** 0 new. Host PRs still open. Expanded Stirling-PDF/drawio/Mermaid → 10/10 core-host/packaging. Updated LOOP idle rule: after 3+ all-kill expands with ready OUTREACH, prefer revalidate/outreach over more host trackers. Still awaiting personal sends.

**Idle note (2026-07-30b):** 0 new intake. Host PRs still open. Expanded Memos/Joplin/Standard Notes → 5/5 packaging/core-host kills. No new public emails for secondary leads; noted @gitekDev site. Prefer personal OUTREACH sends (#1–#4 + Aaron).

**Idle note (2026-07-30a):** 0 new intake. Host PRs #5797/#42346 + all 4 live sources still open. Expanded Daytona/Gitpod/vCluster/Ptah → 11/11 core-host/packaging/pairwise. Added Aaron LinkedIn/X draft in OUTREACH.md. Prefer personal sends over more remote-dev expands.

**Idle note (2026-07-29r):** Parallel idle work this cycle: (1) revalidated all 4 live cards + host PRs #5797/#42346 — still OPEN; (2) Yaak/Scalar/HTTPie peer expand → 14 core-host kills (HTTPie #222 git-sync is multi-host signal for live card #1, still kill as host feature). OUTREACH still awaits personal inbox send (#1–#4). No more API-client expands.

**Idle note (2026-07-29q):** 0 new. No host expand. Added @riemers `info@hashop.nl` — now **4 ready emails** in OUTREACH.md. Host PRs still open. Blocker is personal inbox send, not more GitHub scanning.

**Idle note (2026-07-29p):** 0 new first pass. Host PRs #5797/#42346 still open/unmerged; live issues #870/#1341/#2389 + discussion #12269 still open. Expanded Lago/OpenMeter/Convoy/Unleash/Matomo/Budibase/Teable/Lightdash → 16/16 core-host/packaging/pairwise/driver kills. Billing+BI trackers also host-feature saturated. Prefer Serhii sending the 3 ready OUTREACH.md emails next.

**Idle note (2026-07-29o):** 1 new (Next.js #43179) → core-host kill. Enriched [`OUTREACH.md`](OUTREACH.md) with public emails for @lauhon, @johnmaguire, @borrelan + copy-paste drafts. Host PRs still open. Prefer Serhii sends those 3 emails next; no more monitoring-host expands.

**Idle note (2026-07-29n):** 0 new first pass; host PRs #5797/#42346 still unmerged. Expanded Gatus/Dockge/Dozzle/Beszel → 15/15 core-host. Prefer sending OUTREACH.md DMs over more monitoring-host expand.

**Idle note (2026-07-29m):** 0 new. Built [`OUTREACH.md`](OUTREACH.md) with named leads + DM drafts from live threads (@lauhon/#870 employer pitch; Coolify #2389 bounty backers @riemers/@johnmaguire; RLS @aaronksaunders; DMARC @borrelan). Prior Duplicati/Borg/Kopia expand was 15/15 core-host — no more backup-CLI spam. Host PRs still open.

**Idle note (2026-07-29l):** 0 new. Design-partner maps for #2–#4 — RLS: DEV/pgTAP authors + Supabase Discord (UI vs pgTAP); DMARC: Mailcow/#1341 + Mailu watchers; Coolify: #2389/#4597 + CoolifyBR/DEV restore authors. Host PRs still unmerged. No GitHub expand this tick. Still 4 live cards.

**Idle note (2026-07-29k):** 0 new. Design-partner pass on #1 — Bruno migration guides + import bugs show a holdout segment (Postman/Hoppscotch users who won't fully migrate). Outreach: Hoppscotch #870, feedback.yaak.app, r/api / DEV threads on Postman→Bruno pain. Host PRs #5797/#42346 still open/unmerged. Expanded Neon/Electric/libSQL for multi-Postgres RLS peer signal (not more CI). Still 4 live cards.

**Idle note (2026-07-29j):** Host PR watch on #1–#2 — Hoppscotch #5797 still draft/open; Supabase #42346 still open/unmerged. Expanded Woodpecker/Harbor/pgAdmin → 15 kills (core-host/packaging). Still 4 live cards; next idle prefer outreach, not more CI trackers.

**Idle note (2026-07-29i):** Design-partner pass on #3–#4. DMARC #1341 open — free Postmark/dmarcian tiers crowd basic dashboards; keep for Mailcow-native multi-domain wedge. Coolify #2389 + #4597 open — SimpleBackups $49+/mo proves WTP; Coolify docs still skip app volumes. Expanded NPM/Caddy/Bitwarden/Coder (not more mail/PaaS peers).

**Idle note (2026-07-29h):** Design-partner pass on #1–#2 (not more host-tracker spam). Collection sync: Bruno/Yaak/Insomnia already monetize sync — wedge is multi-client holdouts; #870 + draft PR #5797 still open. RLS: discussion #12269 open; Supabase PR #42346 Playground unmerged; free CLIs (SupaShield/rlsgrid) raise bar. Expanded Yaak/Insomnia peer intake → 15 kills (Insomnia UI/core + CasaOS/Runtipi boards). Runtipi discussion #768 backup/restore = another Coolify-card duplicate signal.

**Idle note (2026-07-29g):** Revalidated Coolify backups #4 — #2389 and discussion #4597 still OPEN. Runtipi #2312 same backup/restore job (killed duplicate). Expanded CasaOS/Umbrel/Runtipi/Yacht peer intake.

**Idle note (2026-07-29f):** Revalidated DMARC card #3 — Mailcow #1341 still OPEN. Mailu #122 DMARC Analyzer is the same job (killed duplicate; strengthens multi-host signal). Discourse expansion largely exhausted. Expanded Postal/Mailu/Modoboa/Roundcube intake.

**Idle note (2026-07-29e):** Added Discourse intake (`harvest_discourse.py`: n8n, rclone, Ghost, Home Assistant, Mattermost). Judged 20 topics — all core-host/pairwise/driver kills. Revalidated RLS card #2 — still OPEN, keep 8/10. Public Canny/Featurebase still blocked.

**Idle note (2026-07-29d):** Revalidated #1 collection sync — Hoppscotch #870 still OPEN (updated 2026-03-24). Draft PR #5797 exists but unmerged; Bruno remains the main workaround. Multi-client git-sync wedge still passes. Probed public Canny/Featurebase boards: most Canny subdomains `notFound`, Featurebase often private/401 — connector still blocked. Expanded Bruno/Kong/cloudflared/search/auth intake.

**Idle note (2026-07-29):** Judged 61 news (chat/git/photo/media hosts) — all core-host kills. Expanded Immich/Paperless/rclone/Jellyfin/ntfy intake; still no new ≥8 card. Next: validate collection sync, or seek non-GitHub boards.
