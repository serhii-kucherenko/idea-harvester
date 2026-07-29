# Live cards scorecard

Solo-indie gate (RUBRIC.md). Revalidated each idle tick when intake is empty.

| Card | Score | One-liner | Concierge in a week? | Main risk |
|------|------:|-----------|----------------------|-----------|
| [API collection git sync](cards/hoppscotch-870-feature-sync-collections-with-git-r.md) | 8/10 | Git sync for Hoppscotch/Postman/Insomnia collections | Yes - CLI + GitHub App | Hosts ship native git sync (draft PR #5797) |
| [RLS debugger](cards/supabase-12269-add-feature-to-test-debug-row-level.md) | 8/10 | Test Postgres RLS policies against sample JWTs | Yes - SQL harness + UI | Supabase ships it |
| [DMARC reports](cards/mailcow-dockerized-1341-feature-request-dmarc-report-parser.md) | 8/10 | Cheap DMARC dashboard for self-hosted mail | Yes - parse rua mailbox | Enterprise DMARC suites / Mailcow UI |
| [Coolify backups](cards/coolify-2389-feature-backup-manger-in-the-ui.md) | 8/10 | Scheduled backups/restore for self-hosted PaaS | Yes - S3 + restore drills | Coolify ships good enough backups |

**Pick order for validation:** collection sync → RLS → DMARC → Coolify backups.

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
