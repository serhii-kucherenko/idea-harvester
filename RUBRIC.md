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
