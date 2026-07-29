# [Feature]: Backup Manger in the UI

source: https://github.com/coollabsio/coolify/issues/2389
repo: coollabsio/coolify
+1s: 36 | comments: 42 | opened: 2024-06-08
score: 8/10
dimensions: standalone=2 wtp=2 host-risk=1 solo-ship=2 distribution=1
scored: 2026-07-29

## Gap
Self-hosted PaaS users (Coolify and peers) want reliable, UI-simple backups and restores without wiring their own S3 cron scripts.

## Why host won't
Coolify issue open with sustained votes asking for a Backup Manager in the UI; meanwhile operators hack schedules by hand. Even if Coolify ships a basic UI later, multi-host backup remains a job.

## Product angle
Solo SaaS: connect Coolify (then CapRover/Dokploy/raw Docker) → scheduled encrypted backups to the customer's S3/R2 → one-click restore drills + alerts. Concierge week 1 as manual restore runbooks; automate after.

## Competition / workarounds
SimpleBackups ($49–299/mo — proves WTP for Docker/server backups), DIY restic/cron, Coolify’s own instance/S3 backup (docs: does **not** cover app volume data). Wedge is Coolify/Dokploy-native volume+app restore drills cheaper/simpler than SimpleBackups for indie hosters.

## Kill if
Coolify ships excellent native app-volume backup+restore that removes willingness to pay, or <3 paying design partners after concierge.

## Tick note
Revalidated 2026-07-29i: #2389 still OPEN (updated 2026-06-25); discussion #4597 still OPEN (68↑, updated 2026-07-15). Design-partner note: pitch restore confidence vs SimpleBackups price floor. Score 8/10 — keep.

## Related signal
Also see Coolify discussion [Backup Docker Volumes](https://github.com/coollabsio/coolify/discussions/4597) (68 upvotes) - same backup/restore job.
Runtipi [general backup/restore option in the UI](https://github.com/runtipi/runtipi/issues/2312) asks for the same job — killed as duplicate; strengthens multi-host PaaS backup wedge.
Nginx Proxy Manager [Backup from WebGui](https://github.com/NginxProxyManager/nginx-proxy-manager/issues/168) asks for the same job — killed as duplicate; strengthens multi-host ops backup wedge.
