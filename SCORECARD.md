# Live cards scorecard

Solo-indie gate (RUBRIC.md). Revalidated each idle tick when intake is empty.

| Card | Score | One-liner | Concierge in a week? | Main risk |
|------|------:|-----------|----------------------|-----------|
| [API collection git sync](cards/hoppscotch-870-feature-sync-collections-with-git-r.md) | 9/10 | Git sync for Hoppscotch/Postman/Insomnia collections | Yes - CLI + GitHub App | Hosts ship native git sync |
| [RLS debugger](cards/supabase-12269-add-feature-to-test-debug-row-level.md) | 8/10 | Test Postgres RLS policies against sample JWTs | Yes - SQL harness + UI | Supabase ships it |
| [DMARC reports](cards/mailcow-dockerized-1341-feature-request-dmarc-report-parser.md) | 8/10 | Cheap DMARC dashboard for self-hosted mail | Yes - parse rua mailbox | Enterprise DMARC suites / Mailcow UI |
| [Coolify backups](cards/coolify-2389-feature-backup-manger-in-the-ui.md) | 8/10 | Scheduled backups/restore for self-hosted PaaS | Yes - S3 + restore drills | Coolify ships good enough backups |

**Pick order for validation:** collection sync → RLS → DMARC → Coolify backups.

**Idle note (2026-07-26):** Killed LLM docs pack - free `llms.txt` / `llms-full.txt` generators crowded the wedge.
