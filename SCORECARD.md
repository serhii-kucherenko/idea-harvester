# Live cards scorecard

Solo-indie gate (RUBRIC.md). Revalidated each idle tick when intake is empty.

| Card | Score | One-liner | Concierge in a week? | Main risk |
|------|------:|-----------|----------------------|-----------|
| [LLM docs pack](cards/tailwindcss-14677-documentation-as-a-single-file-for.md) | 9/10 | Pack any docs site into one LLM-friendly file | Yes - CLI + 5 OSS packs | llm.txt becomes free default |
| [RLS debugger](cards/supabase-12269-add-feature-to-test-debug-row-level.md) | 8/10 | Test Postgres RLS policies against sample JWTs | Yes - SQL harness + UI | Supabase ships it |
| [API collection git sync](cards/hoppscotch-870-feature-sync-collections-with-git-r.md) | 9/10 | Git sync for Hoppscotch/Postman/Insomnia collections | Yes - CLI + GitHub App | Hosts ship native git sync |
| [Coolify backups](cards/coolify-2389-feature-backup-manger-in-the-ui.md) | 8/10 | Scheduled backups/restore for self-hosted PaaS | Yes - S3 + restore drills | Coolify ships good enough backups |
| [DMARC reports](cards/mailcow-dockerized-1341-feature-request-dmarc-report-parser.md) | 8/10 | Cheap DMARC dashboard for self-hosted mail | Yes - parse rua mailbox | Enterprise DMARC suites / Mailcow UI |

**Pick order for validation:** docs pack → collection sync → RLS → DMARC → Coolify backups.
