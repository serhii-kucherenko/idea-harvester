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
Manual `SET LOCAL ROLE` SQL, SupaShield CLI, rlsgrid, rlsmon, rlsautotest (pgTAP generator), official Supabase pgTAP docs. Supabase open PR #42346 “RLS Policy Playground UI” (unmerged). Free CLIs/docs crowd “basic test harness” — wedge is interactive allow/deny matrix + multi-Postgres CI for builders who bounce off pgTAP.

## Kill if
Supabase merges/ships excellent RLS Playground and paid demand disappears; or free CLIs fully cover CI+matrix needs.

## Tick note
Revalidated 2026-07-29l: #12269 open; PR #42346 still unmerged. Outreach: authors of RLS-testing DEV posts, Supabase Discord #help builders hitting silent RLS fails, discussion #12269 commenters — pitch UI matrix vs writing pgTAP. Score 8/10 — keep.
