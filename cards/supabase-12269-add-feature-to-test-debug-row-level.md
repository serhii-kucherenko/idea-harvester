# Add Feature to Test + Debug Row Level Security Policies

source: https://github.com/orgs/supabase/discussions/12269
repo: supabase/supabase
+1s: 46 | comments: 11 | opened: 2022-06-16
score: 8/10
dimensions: standalone=2 wtp=2 host-risk=1 solo-ship=2 distribution=1
scored: 2026-07-29

## Gap
Postgres/Supabase builders need a safe way to test and debug Row Level Security policies against example roles/JWTs without guessing in production.

## Why host won't
Supabase Feature Request discussion open with strong votes for an RLS test/debug surface; still a pain for app builders.

## Product angle
Solo tool: paste policies + sample JWTs/roles → matrix of allow/deny with explanations. Works against local Postgres or Supabase project. Concierge: manually review 5 customers’ policies in week 1.

## Competition / workarounds
Manual `SET LOCAL ROLE` SQL, SupaShield CLI (supashield.app, ~100★), rlsgrid (cross-tenant fuzzer), rlsmon, Studio SQL impersonation docs. Supabase open PR #42346 “RLS Policy Playground UI” (unmerged as of 2026-02). Wedge is CI-grade multi-Postgres + clearer UX than CLI-only tools — host shipping Studio playground would shrink host-risk fast.

## Kill if
Supabase merges/ships excellent RLS Playground and paid demand disappears; or free CLIs fully cover CI+matrix needs.

## Tick note
Revalidated 2026-07-29h: discussion #12269 still OPEN (updated 2026-07-10, 46 upvotes). PR #42346 open/unmerged — host-risk stays 1, not host-shipped yet. Score 8/10 — keep; watch #42346.
