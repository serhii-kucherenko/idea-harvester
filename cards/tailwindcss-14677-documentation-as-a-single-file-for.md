# Documentation as a single file for LLM use

source: https://github.com/tailwindlabs/tailwindcss/discussions/14677
repo: tailwindlabs/tailwindcss
+1s: 121 | comments: 54 | opened: 2024-10-15
score: 9/10
dimensions: standalone=2 wtp=2 host-risk=2 solo-ship=2 distribution=2
scored: 2026-07-26

## Gap
Teams want library/framework docs as one LLM-friendly file instead of crawling dozens of pages.

## Why host won't
Tailwind Ideas thread (121 upvotes) asks for a single-file docs dump; maintainers have not made this a productized export across ecosystems.

## Product angle
Solo SaaS/CLI: point at any docs site or GitHub docs folder → produce a versioned, token-efficient single file / pack for Cursor/ChatGPT. Start with popular OSS docs; charge per seat for private docs packs + refresh.

## Competition / workarounds
Manual curl/wget, Firecrawl, site-to-md scripts. Wedge is curated OSS packs + private docs refresh + LLM-oriented formatting.

## Kill if
Major docs hosts ship first-class llm.txt everywhere and willingness to pay collapses, or <3 paying users after concierge.
