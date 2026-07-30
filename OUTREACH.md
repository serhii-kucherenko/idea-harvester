# Design-partner outreach queue

Execute from SCORECARD pick order. Do not spam issue threads with product pitches —
prefer polite email / LinkedIn after a useful comment, or reply offering a free concierge.

## Send today (priority)

| # | Lead | Contact | Card | Status |
|---|------|---------|------|--------|
| 1 | @lauhon (Laurenz Honauer) | laurenz.honauer@gmail.com · [gh](https://github.com/lauhon) · [site](https://getnewfinance.com) | Collection sync | **ready** — public email |
| 2 | @johnmaguire (John Maguire) | contact@johnmaguire.me · [gh](https://github.com/johnmaguire) · [site](https://www.johnmaguire.me/) | Coolify backups | **ready** — public email + bounty |
| 3 | @borrelan (Andre B) | borrelan@gmail.com · [gh](https://github.com/borrelan) | DMARC | **ready** — public email |
| 4 | @riemers (Erik-jan Riemers) | info@hashop.nl · [gh](https://github.com/riemers) · [hashop.nl](https://hashop.nl) | Coolify backups | **ready** — site mailto + $150 bounty |
| 5 | @aaronksaunders | no public email · [gh](https://github.com/aaronksaunders) · [LinkedIn](https://www.linkedin.com/in/aaronksaunders/) · [X](https://x.com/aaronksaunders) · [linktree](https://linktr.ee/aaronksaunders) | RLS | LinkedIn / X |

Do **not** auto-blast from the harvest bot. Send as yourself (Serhii) from a personal inbox so replies land correctly. Log sent/replied below.

### Send checklist (personal inbox)

1. Copy draft #1 → laurenz.honauer@gmail.com (collection sync)
2. Copy draft #2 → contact@johnmaguire.me (Coolify encrypted backups)
3. Copy draft #3 → borrelan@gmail.com (DMARC)
4. Copy draft #4 → info@hashop.nl (Coolify WP bounty)
5. Paste LinkedIn/X draft → @aaronksaunders (RLS)
6. Mark each row in the Sent log when done

### Email drafts

**To laurenz.honauer@gmail.com — subject: Hoppscotch git sync without switching clients**

> Hi Laurenz — saw your note on Hoppscotch #870 about git sync being the blocker to pitch at work. I’m testing a tiny sidecar that keeps API collections in git without forcing a Bruno migration. Would you try it on one collection this week for free?

**To contact@johnmaguire.me — subject: Coolify encrypted volume backups (free restore drill)**

> Hi John — saw your bounty note on Coolify #2389 about encrypted backups. I’m running free restore drills for a few Coolify hosts this month (volumes + encrypt-at-rest). Want one on a non-prod box?

**To borrelan@gmail.com — subject: Mailcow-friendly DMARC digest**

> Hi Andre — saw your notes on Mailcow #1341 wanting something stitched to the platform rather than raw parsedmarc. I’m prototyping a cheap multi-domain DMARC digest aimed at self-hosted mail. Open to a free pilot on one domain?

**To info@hashop.nl (Erik-jan / @riemers) — subject: Coolify WordPress volume backups**

> Hi Erik-jan — saw your $150 bounty on Coolify #2389 for easy WordPress volume backup/restore. I’m offering free restore drills on a non-prod Coolify host this month. Want one, or should I aim the pilot at the bounty scope directly?

**LinkedIn / X to @aaronksaunders — RLS allow/deny matrix**

> Hi Aaron — saw your ask on the Supabase RLS debug thread for a UI to test policies against roles/JWTs. I’m prototyping an allow/deny matrix (paste policies + sample JWTs) that works against local Postgres or a Supabase project. Open to a free policy review on one project this week?

---

## 1) Collection sync (Hoppscotch #870)

| Lead | Why | Angle |
|------|-----|-------|
| @lauhon | Wants to pitch employer; git sync is the blocker | Multi-client git sync without forcing Bruno migration |
| @ImNicolasTheDev | Still asking after 4+ years | Concierge: sync their Hoppscotch collection to a private repo |
| @federicorosso1993 | “Only thing missing” while evaluating | Same — one-collection pilot |
| @nazimuddintbasha | Notes interest vs no movement | Soft ask: would they try a sidecar? |

Skip: @Bigua / Bruno converts (already solved via Bruno).

## 2) RLS debugger (Supabase #12269)

| Lead | Why | Angle |
|------|-----|-------|
| @aaronksaunders | Explicitly wants UI to test/debug policies | Interactive allow/deny matrix |
| @munaf-khatri | Built rlsautotest; knows the pain | Partner/complement (UI on top of generators) — careful not to compete awkwardly |
| Discussion voters (46↑) | Open since 2022 | Concierge policy review |

Watch: Supabase PR #42346 (still unmerged as of 2026-07-29).

## 3) DMARC (Mailcow #1341)

| Lead | Why | Angle |
|------|-----|-------|
| @borrelan | Wants platform-stitched, not external DIY | Mailcow-native onboarding |
| @ThomDietrich | Keeps issue open; summarized need | Cheap digest vs parsedmarc stack |
| @schw4rzlicht | 2026 deliverability pressure | Multi-domain digest |

Skip pitching @dragoangel (already ships parsedmarc compose — competitor/workaround).

## 4) Coolify backups (#2389)

| Lead | Why | Angle |
|------|-----|-------|
| @riemers | **$150 bounty** — WordPress volumes | Volume backup + easy restore |
| @johnmaguire | Bounty — encrypted backups must-have | Encrypted S3 restore drills |
| @wowtah / @gitekDev | Production blocker; SFTP backup | Managed restore confidence · @gitekDev site [xoose.de](https://www.xoose.de) (no public email found) |
| @Holo795 | Already built OSS workaround | Learn wedge; maybe not a buyer |

---

## Sent log

| When | Who | Channel | Result |
|------|-----|---------|--------|
| — | — | — | none sent yet (tick 41: still awaiting personal inbox / LinkedIn) |

Updated: 2026-07-30 (tick 41).
