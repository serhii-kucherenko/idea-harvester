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
Bruno (git-native), Postman cloud sync, manual JSON in git, Insomnia git sync (partial). Wedge is multi-client + clean diffs for teams not switching clients.

## Kill if
Hoppscotch ships excellent native git sync AND multi-client users still will not pay; or <3 design partners after concierge.

## Tick note
Revalidated 2026-07-29: issue still OPEN; host-risk lowered (draft PR in flight). Score 8/10 — keep.
