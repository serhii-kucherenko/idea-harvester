# Feature Request: DMARC report parser

source: https://github.com/mailcow/mailcow-dockerized/issues/1341
repo: mailcow/mailcow-dockerized
+1s: 27 | comments: 34 | opened: 2018-04-30
score: 8/10
dimensions: standalone=2 wtp=2 host-risk=2 solo-ship=2 distribution=1
scored: 2026-07-29

## Gap
Self-hosted mail admins (Mailcow and peers) get raw DMARC aggregate reports and need readable pass/fail/fail-source dashboards without buying enterprise email security suites.

## Why host won't
Mailcow feature request for a DMARC report parser stays open; operators still forward XML to third parties or ignore reports.

## Product angle
Solo SaaS: drop a mailbox/API for DMARC rua reports → parse → weekly digest + simple domain dashboard. Start Mailcow-friendly docs, then any self-hosted MTA. Concierge: manually parse a customer's last 30 days of reports in week 1.

## Competition / workarounds
Postmark DMARC (free digests), dmarcian/EasyDMARC free tiers + ~$8–25/mo paid, Cloudflare DMARC Management, parsedmarc (self-host + ELK). Free tiers crowd “basic dashboard” WTP — wedge is Mailcow/self-host MTA onboarding + multi-domain digest without enterprise SOC, not beating Postmark on price alone.

## Kill if
Mailcow ships a good enough built-in parser; free SaaS digests absorb the Mailcow segment; or <3 paying admins after concierge.

## Tick note
Revalidated 2026-07-29i: #1341 still OPEN (updated 2026-02-21). Design-partner note: start outreach with multi-domain self-hosters who already tried Postmark/parsedmarc and still want a Mailcow-native flow. Score 8/10 — keep.

## Related signal
Mailu [DMARC Analyzer](https://github.com/Mailu/Mailu/issues/122) asks for the same job — killed as duplicate; strengthens multi-host DMARC wedge.
