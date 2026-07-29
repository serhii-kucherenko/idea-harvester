# [feature]: Sync Collections with Git repo

source: https://github.com/hoppscotch/hoppscotch/issues/870
repo: hoppscotch/hoppscotch
+1s: 106 | comments: 68 | opened: 2020-05-13
score: 8/10
dimensions: standalone=2 wtp=2 host-risk=1 solo-ship=2 distribution=1
scored: 2026-07-29

## Gap
API teams want collections versioned in Git and shared across machines/clients without vendor lock-in to one client UI.

## Why host won't
Open Hoppscotch request since 2020 with 100+ reactions; draft PR #5797 (Jan 2026) exists but unmerged. Same pain remains for Postman/Insomnia users who outgrow vendor sync.

## Product angle
Solo SaaS/CLI: export/import + continuous sync of API collections (Hoppscotch/Postman/Insomnia formats) to a Git repo, with PR-friendly diffs and team invite. Start CLI + GitHub App; charge per seat for sync + conflict UI.

## Competition / workarounds
Bruno (git-native; Pro ~$6/user/mo), Yaak (local files + Git; commercial license), Insomnia Git sync (paid tiers), Thunder Client Pro, Postman cloud. Paid seats prove WTP for sync/collab — but free git-native clients crowd a pure “git sync for one host” wedge. Still viable as multi-client bridge for teams stuck on Postman/Hoppscotch who will not migrate.

## Kill if
Hoppscotch ships excellent native git sync AND multi-client users still will not pay; or <3 design partners after concierge; or Bruno/Yaak absorb the non-migrating segment.

## Tick note
Revalidated 2026-07-29k: #870 + draft PR #5797 unchanged. Outreach map: target Postman/Hoppscotch teams blocked by Bruno migration friction (script translator gaps, folder-import bugs like #7821) — not Bruno converts. Channels: Hoppscotch #870 thread, Yaak feedback (https://feedback.yaak.app reachable), r/api, Bruno Discussions migrants who bounced. Score 8/10 — keep.
