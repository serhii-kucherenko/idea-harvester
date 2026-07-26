# [Feature]: Backup Manger in the UI

source: https://github.com/coollabsio/coolify/issues/2389
repo: coollabsio/coolify
+1s: 36 | comments: 42 | opened: 2024-06-08
score: 8/10
dimensions: standalone=2 wtp=2 host-risk=1 solo-ship=2 distribution=1
scored: 2026-07-26

## Gap
Self-hosted PaaS users (Coolify and peers) want reliable, UI-simple backups and restores without wiring their own S3 cron scripts.

## Why host won't
Coolify issue open with sustained votes asking for a Backup Manager in the UI; meanwhile operators hack schedules by hand. Even if Coolify ships a basic UI later, multi-host backup remains a job.

## Product angle
Solo SaaS: connect Coolify (then CapRover/Dokploy/raw Docker) → scheduled encrypted backups to the customer's S3/R2 → one-click restore drills + alerts. Concierge week 1 as manual restore runbooks; automate after.

## Competition / workarounds
SimpleBackups, Veeam-ish tools, DIY restic/cron. Wedge is Coolify-native UX + restore confidence for indie hosters.

## Kill if
Coolify ships excellent native backup+restore that removes willingness to pay, or <3 paying design partners after concierge.

## Tick note
Revalidated 2026-07-26: still open gap; solo bar still passes.

## Related signal
Also see Coolify discussion [Backup Docker Volumes](https://github.com/coollabsio/coolify/discussions/4597) (68 upvotes) - same backup/restore job.
