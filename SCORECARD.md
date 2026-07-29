# Live cards scorecard

Solo-indie gate (RUBRIC.md). Revalidated each idle tick when intake is empty.

| Card | Score | One-liner | Concierge in a week? | Main risk |
|------|------:|-----------|----------------------|-----------|
| [API collection git sync](cards/hoppscotch-870-feature-sync-collections-with-git-r.md) | 8/10 | Git sync for Hoppscotch/Postman/Insomnia collections | Yes - CLI + GitHub App | Hosts ship native git sync (draft PR #5797) |
| [RLS debugger](cards/supabase-12269-add-feature-to-test-debug-row-level.md) | 8/10 | Test Postgres RLS policies against sample JWTs | Yes - SQL harness + UI | Supabase ships it |
| [DMARC reports](cards/mailcow-dockerized-1341-feature-request-dmarc-report-parser.md) | 8/10 | Cheap DMARC dashboard for self-hosted mail | Yes - parse rua mailbox | Enterprise DMARC suites / Mailcow UI |
| [Coolify backups](cards/coolify-2389-feature-backup-manger-in-the-ui.md) | 8/10 | Scheduled backups/restore for self-hosted PaaS | Yes - S3 + restore drills | Coolify ships good enough backups |

**Pick order for validation:** collection sync → RLS → DMARC → Coolify backups.

**Idle note (2026-07-29e):** Added Discourse intake (`harvest_discourse.py`: n8n, rclone, Ghost, Home Assistant, Mattermost). Judged 20 topics — all core-host/pairwise/driver kills. Revalidated RLS card #2 — still OPEN, keep 8/10. Public Canny/Featurebase still blocked.

**Idle note (2026-07-29d):** Revalidated #1 collection sync — Hoppscotch #870 still OPEN (updated 2026-03-24). Draft PR #5797 exists but unmerged; Bruno remains the main workaround. Multi-client git-sync wedge still passes. Probed public Canny/Featurebase boards: most Canny subdomains `notFound`, Featurebase often private/401 — connector still blocked. Expanded Bruno/Kong/cloudflared/search/auth intake.

**Idle note (2026-07-29):** Judged 61 news (chat/git/photo/media hosts) — all core-host kills. Expanded Immich/Paperless/rclone/Jellyfin/ntfy intake; still no new ≥8 card. Next: validate collection sync, or seek non-GitHub boards.
