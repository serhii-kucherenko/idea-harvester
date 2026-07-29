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
Manual SQL, ad-hoc scripts, eventual first-party Supabase UI. Wedge is better DX + multi-Postgres later.

## Tick note
Revalidated 2026-07-29: discussion still OPEN via GitHub API; solo bar still passes.
