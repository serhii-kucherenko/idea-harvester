# Design-partner outreach queue

Execute from SCORECARD pick order. Do not spam issue threads with product pitches —
prefer polite DMs / email after a useful comment, or reply offering a free concierge.

## 1) Collection sync (Hoppscotch #870)

| Lead | Why | Angle |
|------|-----|-------|
| @lauhon | Wants to pitch employer; git sync is the blocker | Multi-client git sync without forcing Bruno migration |
| @ImNicolasTheDev | Still asking after 4+ years | Concierge: sync their Hoppscotch collection to a private repo |
| @federicorosso1993 | “Only thing missing” while evaluating | Same — one-collection pilot |
| @nazimuddintbasha | Notes interest vs no movement | Soft ask: would they try a sidecar? |

Skip: @Bigua / Bruno converts (already solved via Bruno).

**First message (DM):** “Saw your note on Hoppscotch #870 about git sync for work. I’m testing a tiny sidecar that keeps collections in git without switching clients — would you try it on one collection this week for free?”

## 2) RLS debugger (Supabase #12269)

| Lead | Why | Angle |
|------|-----|-------|
| @aaronksaunders | Explicitly wants UI to test/debug policies | Interactive allow/deny matrix |
| @munaf-khatri | Built rlsautotest; knows the pain | Partner/complement (UI on top of generators) — careful not to compete awkwardly |
| Discussion voters (46↑) | Open since 2022 | Concierge policy review |

**First message:** “Working on a small RLS allow/deny matrix (paste policies + JWT → green/red). Would you let me run it against a throwaway project copy this week?”

Watch: Supabase PR #42346 (still unmerged).

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
| @wowtah / @gitekDev | Production blocker; SFTP backup | Managed restore confidence |
| @Holo795 | Already built OSS workaround | Learn wedge; maybe not a buyer |

**First message:** “Saw your Coolify #2389 note / bounty on volume+encrypted backups. I’m running free restore drills for 3 Coolify hosts this month — want one?”

---

Updated: 2026-07-29 (tick 26). Prefer DMs over public spam. Log replies back into this file.
