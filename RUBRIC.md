# Solo indie rubric

Target: one founder, ship value in weeks, strangers pay monthly.

A tracker upvote is a **pain quote**, not a company. Card only if the gap is a
workflow you can sell **without** the host's permission or marketplace.

## Score (0–2 each, card if ≥ 8/10)

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **standalone** | Only useful inside host UI/API | Sidecar that still needs host daily | Job done even if host never changes |
| **wtp** | Expect free / OSS plugin | Maybe pay once | Already pay for worse workaround (agency, Zapier, spreadsheet tax) |
| **host-risk** | Host can erase you in one release | Host might ship in 1–2 years | Multi-host job or host publicly refused for structural reasons |
| **solo-ship** | Needs team / heavy infra | Stretch for one person in a month | Concierge in under a week, automate after |
| **distribution** | Need host marketplace charity | Thin SEO/community path | Clear channels (communities, ads, content) to buyers |

### Hard fail → kill immediately

- Pairwise integrations (A↔B sync, “add Slack but for X”)
- Host drivers/plugins as the product
- Core host engine/UI features
- Infra that needs multi-tenant query engines on day one
- Self-host / Docker / packaging requests
- One-shot migration/export utilities (no monthly buyer)

## Rubric deltas

- **2026-08-02a:** HA Airtouch 5 integration - pairwise device-driver kill. HVAC/host device integrations stay HA work.
- **2026-08-01c:** Open WebUI #11884 forgot-password + HA Hydrawise sprinkler - core-host auth and pairwise device-driver kills. Chat-UI auth and HA device integrations stay host work.
- **2026-08-01a:** Mattermost #30126 Matterbridge support - pairwise kill. Chat-bridge A↔B stays host ecosystem work.
- **2026-07-31t:** Immich #7262 Ultra HDR on Android - core-host kill. Photo-library mobile decode/display stays host UI.
- **2026-07-31s:** TanStack Router #2701 test server functions - core-host kill. Framework DX/testing stays with the host.
- **2026-07-31q:** Plane #2648 n8n/workflow integration - pairwise kill. Host↔automation-tool sync is not a solo wedge.
- **2026-07-31i:** Twenty #7296 WhatsApp Business sync - pairwise integration kill. CRM↔messenger sync stays host marketplace work.
- **2026-07-31d:** Immich #2155 mobile upload-status filter - core-host kill. Photo-library mobile UX stays host UI.
- **2026-07-31b:** Sentry #84596 mobile replay network bodies - core-host kill. Session-replay host features stay host UI.
- **2026-07-31a:** Open WebUI/Immich board news - 4/4 core-host or driver. Photo-library + chat-UI trackers still host-feature saturated.
- **2026-07-30x:** Idle 0 new — skipped expand; removed duplicate sentinel; PRs open; waiting on OUTREACH sends.
- **2026-07-30w:** Idle 0 new — skipped expand; removed duplicate sentinel; PRs open; waiting on OUTREACH sends.
- **2026-07-30v:** Idle 0 new — skipped expand; removed duplicate sentinel; PRs open; waiting on OUTREACH sends.
- **2026-07-30u:** Idle 0 new — skipped expand; removed duplicate sentinel; PRs open; waiting on OUTREACH sends.
- **2026-07-30t:** Idle 0 new — skipped expand; removed duplicate sentinel; PRs open; waiting on OUTREACH sends.
- **2026-07-30s:** Idle 0 new — skipped expand; removed duplicate sentinel again; PRs open; waiting on OUTREACH sends.
- **2026-07-30r:** Idle 0 new — skipped expand; deduped duplicate harvest sentinel; PRs open; waiting on OUTREACH sends.
- **2026-07-30q:** Idle 0 new - skipped expand; PRs open; waiting on OUTREACH sends.
- **2026-07-30p:** Idle 0 new — promoted 4 live cards to eternal/ideas (first promotion path). Skipped expand; PRs open; waiting on OUTREACH sends.
- **2026-07-30o:** Idle 0 new — skipped expand; PRs open; waiting on OUTREACH sends.
- **2026-07-30n:** Immich .nomedia/.immichignore discussion → core-host kill. Skipped expand; waiting on OUTREACH sends.
- **2026-07-30m:** Idle 0 new — skipped expand; PRs open; waiting on OUTREACH sends.
- **2026-07-30l:** Idle 0 new — skipped expand; PRs open; waiting on OUTREACH sends.
- **2026-07-30k:** Idle 0 new — skipped expand; PRs open; waiting on OUTREACH sends.
- **2026-07-30j:** Immich WebDAV discussion → host-driver kill. Skipped expand; waiting on OUTREACH sends.
- **2026-07-30i:** Idle 0 new — skipped expand; PRs open; waiting on OUTREACH sends.
- **2026-07-30h:** Immich thumbnail-icons discussion → core-host kill. Skipped expand; waiting on OUTREACH sends.
- **2026-07-30g:** Idle 0 new — skipped expand; PRs open; waiting on OUTREACH sends.
- **2026-07-30f:** Idle 0 new — skipped expand; PRs open; no machine progress until OUTREACH sends land.
- **2026-07-30e:** Idle 0 new — skipped expand; PRs still open; no new lead emails. Machine idle is correctly waiting on human OUTREACH sends.
- **2026-07-30d:** Idle 0 new — skipped expand per LOOP (3+ all-kill streak). Revalidated live cards/PRs still open. OUTREACH send checklist added. Value is human send only.
- **2026-07-30c:** Stirling-PDF/Mermaid expand: 10/10 core-host/packaging. LOOP idle now allows skipping expand after 3+ all-kill expands when OUTREACH is ready. Prefer personal sends.
- **2026-07-30b:** Joplin/Memos/Standard Notes expand: 5/5 packaging or core-host. Notes apps same trap. Prefer OUTREACH personal sends.
- **2026-07-30a:** Daytona/Gitpod/vCluster expand: 11/11 core-host, packaging, or pairwise. Remote-dev trackers same trap. Prefer OUTREACH personal sends (4 emails + Aaron LinkedIn draft).
- **2026-07-29r:** Idle revalidation (all 4 live + host PRs still open) plus Scalar/HTTPie/Postman expand 14/14 core-host. HTTPie #222 strengthens collection-sync demand; still not a new card. Prefer OUTREACH human send over more client-tracker expands.
- **2026-07-29q:** Idle 0 new — no expand. OUTREACH now 4 ready emails (added hashop.nl for Coolify bounty lead). Machine work is saturated; value is human send.
- **2026-07-29p:** Lago/Matomo/Teable/Lightdash expand: 16/16 core-host, packaging, pairwise, or driver. Billing/BI/Airtable-clone trackers look like the same core-host trap as PaaS/monitoring. Prefer OUTREACH.md human sends over more product-tracker expands.
- **2026-07-29o:** Idle mostly empty — 1 Next.js discussion kill (core-host). OUTREACH.md now has public emails + drafts for lauhon/johnmaguire/borrelan. Prefer human send from personal inbox; do not bot-blast.
- **2026-07-29n:** Gatus/Dockge/Beszel intake: 15/15 core-host. Monitoring feature trackers still host UX. Prefer OUTREACH.md DMs over more monitoring-host expands.
- **2026-07-29m:** Idle 0 new after Duplicati/Borg/Kopia 15/15 core-host. Executed outreach → OUTREACH.md named leads (Hoppscotch #870, Coolify #2389 bounty commenters, RLS/DMARC). Prefer sending DMs next over more backup-CLI expands.
- **2026-07-29l:** Idle 0 new — design-partner outreach maps for RLS/DMARC/Coolify (skipped another host-tracker expand). New competition notes: rlsautotest + CoolifyBR/Vaultkeeper DIY; free/OSS workarounds raise the bar but don't kill multi-host managed wedges yet.
- **2026-07-29k:** Idle 0 new — design-partner outreach mapping for collection-sync + Neon/Electric/libSQL expand (14/14 core-host; no RLS-debugger wedge). Host PRs #5797/#42346 still unmerged. Prefer #1 outreach over more DB/CI host trackers.
- **2026-07-29j:** Idle 0 new — re-watched Hoppscotch #5797 + Supabase #42346 (both still unmerged). Expanded Woodpecker/Harbor/pgAdmin → 15/15 core-host or packaging kills. No new ≥8. Prefer live-card outreach over more CI/registry trackers next idle.
- **2026-07-29i:** Idle 0 new — validated DMARC + Coolify. Free DMARC SaaS digests (Postmark etc.) weaken “cheap dashboard” WTP; keep only with Mailcow-native multi-domain angle. SimpleBackups $49+/mo strengthens Coolify backup WTP while Coolify still skips app volumes. Next expand: proxy/cert/secrets/remote-dev peers, not more mail/PaaS.
- **2026-07-29h:** Idle 0 new → design-partner validation on live #1–#2, then Yaak/Insomnia expand. 15 judged: Insomnia 5/5 core-host UI; boards 10/10 core-host/packaging; Runtipi #768 backup/restore duplicates Coolify card (again). No new ≥8. Collection-sync WTP proven via Bruno/Insomnia paid sync, but free git-native clients crowd single-host sync. RLS: open host PR #42346 + OSS CLIs raise bar without kill yet.
- **2026-07-29g:** Self-host PaaS peers (CasaOS/Umbrel/Runtipi/Yacht): 14 judged — Runtipi #2312 backup/restore UI duplicates live Coolify card (positive multi-host signal). Rest core-host/packaging. Revalidated Coolify #2389 still open.
- **2026-07-29f:** Mail-stack expand (Postal/Mailu/Modoboa/Roundcube): 16 judged — Mailu #122 DMARC Analyzer is duplicate of live Mailcow DMARC card (positive multi-host signal). Rest core-host/packaging. Revalidated Mailcow #1341 still open.
- **2026-07-29e:** First Discourse intake (n8n/Ghost/HA/Mattermost): 20/20 core-host, pairwise, device-driver, or packaging. Still prefer multi-host ops wedges over product-forum feature votes.
- **2026-07-29d:** Idle with 0 new: probed public Canny/Featurebase boards — Canny subdomains mostly `company.notFound`, Featurebase often private/401. Revalidated collection-sync card (draft Hoppscotch PR #5797 → host-risk↓, still ≥8). Bruno/cloudflared/Authelia/Vikunja/Meilisearch/Typesense intake: 36/36 core-host/packaging.
- **2026-07-29c:** Observability/session-replay/forms intake (Inngest, SigNoz, OpenObserve, OpenReplay, Highlight, HeyForm, Ghost, Fider, Sentry boards): 37/37 core-host, pairwise, or packaging. Git-sync dashboards inside OpenObserve still host UI, not a new solo wedge. Next idle: public Canny/Featurebase-style boards or vertical ops pain outside host trackers.
- **2026-07-29b:** Polar / better-auth / Backrest / Syncthing / restic / filebrowser intake: 21/21 core-host or packaging (auth API, sync engine, restic CLI, Backrest UI). Fleet-backup ask inside Backrest duplicates Coolify backup wedge — keep multi-host ops cards, don't re-card host UI. Next idle: public vote boards / G2-style pain, not more backup CLI hosts.
- **2026-07-29:** Uptime-Kuma / Gitea / Nextcloud / Rocket.Chat shortlists were 100% core-host (API, federation, calendar ACL, messaging UX). Drop dead forgejo search; expand ops-adjacent intake (Immich, Paperless, healthchecks, ntfy, Unkey, Resend).
- **2026-07-26:** After ~200+ GitHub kills, solo cards cluster in multi-host ops wedges (sync/backup/DMARC), not host feature requests. Prefer boards/G2 next.
- **2026-07-25c:** Soften young-repo floors (90d / 5+1s) to fill Top-5 for newer products; solo bar unchanged.
- **2026-07-25b:** Time-tracking / PM adjuncts for a single host (e.g. Plane) fail solo — category already owned by Toggl/Clockify/Harvest.

- **2026-07-25:** Mature GitHub feature trackers skew “make the host better.” Idle ticks must expand intake (younger products, public vote boards), not lower the solo bar.
- **2026-07-25:** `MIN_AGE_DAYS=540` starves products younger than ~18mo — use `sources.json` `young_repos` with softer age/reaction floors, same Top-5 + rubric.

## Card frontmatter

```markdown
source: https://...
score: 8/10
dimensions: standalone=2 wtp=2 host-risk=1 solo-ship=2 distribution=1
scored: YYYY-MM-DD
```

## Kill frontmatter

```markdown
source: https://...
killed: <failing dimension or hard-fail label>
```

## Self-garbage collector

Run each harvest (agent) or `python3 gc_cards.py`:

| Rule | Action |
|------|--------|
| Live `cards/` hard cap **15** | Rank by score, then `scored:` date; demote overflow to `killed/` with `killed: gc-cap` |
| `score` missing or &lt; 8 | Kill (`killed: below-rubric`) |
| `scored:` older than **45 days** and not revalidated | Kill (`killed: stale`) |
| Host shipped it / status changed | Kill (`killed: host-shipped`) |
| Duplicate job across cards | Keep highest score; kill the rest (`killed: duplicate`) |

`killed/` is forever - negative memory for the next run. `cards/` stays small and ranked.
