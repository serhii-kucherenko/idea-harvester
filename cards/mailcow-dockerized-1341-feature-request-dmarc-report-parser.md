# Feature Request: DMARC report parser

source: https://github.com/mailcow/mailcow-dockerized/issues/1341
repo: mailcow/mailcow-dockerized
+1s: 27 | comments: 34 | opened: 2018-04-30
score: 8/10
dimensions: standalone=2 wtp=2 host-risk=2 solo-ship=2 distribution=1
scored: 2026-07-26

## Gap
Self-hosted mail admins (Mailcow and peers) get raw DMARC aggregate reports and need readable pass/fail/fail-source dashboards without buying enterprise email security suites.

## Why host won't
Mailcow feature request for a DMARC report parser stays open; operators still forward XML to third parties or ignore reports.

## Product angle
Solo SaaS: drop a mailbox/API for DMARC rua reports → parse → weekly digest + simple domain dashboard. Start Mailcow-friendly docs, then any self-hosted MTA. Concierge: manually parse a customer's last 30 days of reports in week 1.

## Competition / workarounds
dmarcian, Valimail, Postmark DMARC, DIY scripts. Wedge is cheap, self-host-mailer-friendly onboarding (not enterprise SOC).

## Kill if
Mailcow ships a good enough built-in parser, or <3 paying admins after concierge.

## Tick note
Revalidated 2026-07-26 harvest expand.
