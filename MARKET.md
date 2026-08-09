# SCORECARD market brief

Living doc for **real-world use, demo flow, and pricing** of live/parked MVP wedges.
Updated by the `AGENT_LOOP_TICK_mvp_market` loop (every 10m) and interactive sessions.
Eternal hard gate: every MVP needs a **real UI + runnable demo** (2026-08-09).

Do not invent metrics. Cite public prices / issue threads. Mark confidence.

---

## How to use this file

| Section | Meaning |
|---------|---------|
| Real-world job | Who pays, what they do on Monday |
| Demo flow | Click-path that proves the job (UI required) |
| Pricing | Anchors from competitors + recommended wedge price |
| Gaps | What blocks shipping / WTP proof |
| Next probe | Smallest evidence to kill or keep |

Future ≥8 cards: add a section here before calling MVP Done.

---

## 1) API collection git sync — **active**

**Repo:** `eternal/projects/api-collection-git-sync/repo`  
**Card:** Hoppscotch #870 (106↑, open since 2020; host PR #5797 still **open / unmerged**, last update 2026-01-30 — `gh api` 2026-08-09)

### Real-world application

Teams stuck on Hoppscotch / Postman / Insomnia want collections in **their** git repo for PR review, without migrating the whole client to Bruno. Buyer is often the engineer who already lost a fight to "just use Bruno."

ICP: Postman/Hoppscotch holdouts, not Bruno converts. Adjacent: Yaak already ships plain-file Git sync inside its client (different ICP: people willing to switch clients).

### Demo flow (shipped)

1. `npm run web:dev` → http://localhost:3456  
2. Click **Run sample demo** (or upload Hoppscotch JSON)  
3. See git tree + `??` status + round-trip export JSON  
4. Partner path: `docs/PILOT.md` (CLI) + `docs/PARTNER.md` (keep/kill)

### Pricing (evidence)

| Anchor | Public price | Source / verified |
|--------|--------------|-------------------|
| Bruno Open Source | $0 (GitUI subset; commit/push gated on Pro) | usebruno.com/pricing 2026-08-09 |
| Bruno Pro | **$6/user/mo** billed annually | same (live page) |
| Bruno Ultimate | **$11/user/mo** billed annually | same |
| Yaak Individual (commercial binary) | **$79/year** (~$6.6/mo) or $349 lifetime | yaak.app/pricing 2026-08-09 |
| Yaak Business | **$149/user/year** | same |
| Postman Solo | **$9/mo** annual ($12 monthly) | postman.com/pricing (Mar 2026 plans) |
| Postman Team | **$19/user/mo** annual ($23 monthly); Free = 1 user | same |
| Postman Enterprise | **$49/user/mo** annual | same |

**Recommended wedge (hypothesis, not validated):** free concierge pilot → **$9–15/seat/mo** for multi-client sync + conflict UI, or **$29/mo flat** for solo indie until seats proven. Undercut Postman Team; sit near Bruno Pro / Yaak Individual as "stay in your client" insurance. Yaak proves willingness to pay ~$80/yr for local-first + Git - but that buyer already switched clients.

### Gaps

- Outreach not sent (Laurenz draft in `docs/EVIDENCE.md` / OUTREACH.md)  
- Public npm publish optional; tarball path works  
- Host #5797 may erase Hoppscotch-only wedge; multi-client is the story  

### Next probe

Send Laurenz install-command email; count completed round-trips only.

**Tick:** 2026-08-09b — verified Bruno/Yaak/Postman live prices; #5797 still open.

---

## 2) Postgres RLS debugger — parked MVP (needs UI bar re-check)

**Card:** Supabase discussion #12269  
**Repo:** `postgres-rls-debugger` (CLI + local matrix UI already existed in Phase 3)

### Real-world application

Supabase / Postgres builders paste policies + JWT claims and want an allow/deny matrix before production. Complements pgTAP / CI fuzzers; interactive review is the wedge.

### Demo flow (exists in repo; re-smoke under eternal UI bar)

`node dist/cli.js serve` (README) → paste policies / load fixture → allow/deny matrix. Also CLI: `matrix fixtures/sample.json`. Must stay one-click on cold machine; confirm browser surface still boots before re-parking.

### Pricing (evidence)

| Anchor | Notes |
|--------|-------|
| pgTAP / supabase-test-helpers | Free OSS |
| rlsgrid, SupaShield, rlsautotest | Free OSS CLIs / generators (CI-oriented) |
| Paid security SaaS | No clean public "RLS matrix UI" SaaS price found this tick |

**Recommended wedge:** free local UI forever; optional **$19/mo** cloud paste-and-share for teams, or sponsorship. WTP is weaker than collection-sync until someone pays for convenience over CLI.

### Gaps

Confirm UI still runs; do not re-park without UI+demo pass under new eternal bar.

### Next probe

Re-run `rlsd serve` demo; LinkedIn/X to @aaronksaunders (OUTREACH #5).

**Tick:** 2026-08-09b — confirmed `serve` + matrix in README; browser smoke still next.

---

## 3) Self-host DMARC digest — parked MVP

**Card:** Mailcow #1341  

### Real-world application

Self-hosted mail (Mailcow/Mailu) admins want readable multi-domain DMARC digests without enterprise DMARC suites.

### Demo flow (target)

Drop aggregate XML → HTML digest in browser + optional weekly mail. UI dashboard required under new bar (CLI-only incomplete).

### Pricing (evidence)

| Anchor | Public price | Source / verified |
|--------|--------------|-------------------|
| dmarcian Personal | $0 (≤2 domains, non-business, 1.25k msgs) | dmarcian.com/pricing (2026 reviews + page) |
| dmarcian Basic | **$24/mo** or **$19.99/mo** annual (2 domains, 100k msgs) | same |
| dmarcian Plus | **$240/mo** / **$199/mo** annual (8 domains) | same — steep step at >2 domains |
| dmarcian Enterprise | **$600/mo** / **$499/mo** annual (15 domains, SSO/API) | same |
| Postmark DMARC Digests | **Starts at $14/mo** | postmarkapp.com/pricing add-on 2026-08-09 |

**Recommended wedge:** **$9–15/mo** for ≤5 self-host domains (self-host deploy), or free OSS + paid hosted digest. Compete on Mailcow-native onboarding, not enterprise analytics. Price ceiling is Postmark $14 and dmarcian Basic $20–24; avoid climbing toward Plus ($199+).

### Next probe

Email @borrelan (OUTREACH #3); ship minimal web digest UI before re-calling MVP Done.

**Tick:** 2026-08-09b — dmarcian tiers + Postmark $14 verified.

---

## 4) Coolify volume backups — parked MVP

**Card:** Coolify #2389 (+ bounty signals)

### Real-world application

Coolify operators need encrypted **app volume** backup/restore, not only instance config. Bounty backers already signal cash.

### Demo flow (target)

Web or TUI: pick app → backup → restore drill with green check. CLI-only fails eternal UI bar.

### Pricing (evidence)

| Anchor | Public price | Source / verified |
|--------|--------------|-------------------|
| SimpleBackups Basic | **$0** (1 job, 1 GB) | simplebackups.com/pricing 2026-08-09 |
| SimpleBackups Lite | **$49/mo** (5 jobs, 50 GB, ≤12h) | same (+ AWS Marketplace Essential $49) |
| SimpleBackups Plus | **$99/mo** (20 jobs, 200 GB) | same |
| SimpleBackups Max | **$299/mo** (100 jobs, 1 TB) | same |
| Coolify #2389 bounty | $150 WP volume ask (@riemers) | issue cash signal, not SaaS price |
| Self-host restic/borg | Free; ops tax is the product | — |

**Recommended wedge:** paid restore-drill concierge first; productize at **$15–29/mo** per Coolify host or per N volumes - well under SimpleBackups Lite ($49) if scope stays Coolify-native volumes + one-click restore proof.

### Next probe

Emails to @johnmaguire / @riemers (OUTREACH #2/#4); UI for plan/backup/restore status.

**Tick:** 2026-08-09b — SimpleBackups live tiers filled.

---

## 5) Goal-vs-state delta monitor — parked MVP

**Card:** SCORECARD #5 (internal wedge)

### Real-world application

Surface drift between written goals and reality (webhooks/files) before weekly review fails.

### Demo flow (target)

Dashboard of goals vs last check + notify. Needs UI under new bar.

### Pricing

No strong public SaaS twin priced this tick. Closest: goal trackers / uptime notifiers. Treat as **habit tool**; price after N=1 personal use proves retention.

### Next probe

Personal use for 14 days; then decide keep/kill. Low priority vs #1–#4.

**Tick:** 2026-08-09b — still stub; comps deferred to next tick.

---

## Future cards (template)

When a card scores ≥8 and graduates:

```markdown
## N) <name>
### Real-world application
### Demo flow (UI required)
### Pricing (evidence table)
### Gaps
### Next probe
**Tick:** YYYY-MM-DD
```

---

## Loop state

| Field | Value |
|-------|-------|
| Sentinel | `AGENT_LOOP_TICK_mvp_market` |
| Interval | 10m |
| Last tick | 2026-08-09b |
| Focus next tick | Insomnia Pro live price; RLS `serve` browser smoke; Postmark DMARC Digests domain limits; goal-monitor comps |
