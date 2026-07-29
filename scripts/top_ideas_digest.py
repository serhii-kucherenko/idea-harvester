#!/usr/bin/env python3
"""Build and dedupe email digest payloads for top idea cards.

Usage:
  python scripts/top_ideas_digest.py
  python scripts/top_ideas_digest.py --mark-current-sent
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = ROOT / "cards"
STATE_PATH = ROOT / ".email_digest_state.json"
TOP_N = 5
DEMOS_DIR = ROOT / "demos" / "top-ideas"
GITHUB_REPO = "serhii-kucherenko/idea-harvester"
GITHUB_BRANCH = "main"


def _parse_card(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    title = path.stem
    source = ""
    score = -1
    repo = ""
    dimensions = ""
    sections: dict[str, str] = {}
    current_section = ""
    section_lines: list[str] = []

    def flush_section() -> None:
        if current_section:
            sections[current_section] = "\n".join(section_lines).strip()

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("source:"):
            source = line.split(":", 1)[1].strip()
        elif line.startswith("repo:"):
            repo = line.split(":", 1)[1].strip()
        elif line.startswith("score:"):
            raw = line.split(":", 1)[1].strip()
            score = int(raw.split("/", 1)[0].strip())
        elif line.startswith("dimensions:"):
            dimensions = line.split(":", 1)[1].strip()
        elif line.startswith("## "):
            flush_section()
            current_section = line[3:].strip().lower()
            section_lines = []
        elif line.startswith("## Product angle"):
            continue
        elif current_section:
            section_lines.append(line)

    flush_section()

    if not source:
        return {}
    decision = "PURSUE"
    if score < 8:
        decision = "HOLD"
    if "host-risk=1" in dimensions:
        decision = "PURSUE (time-boxed)"

    return {
        "title": title,
        "source": source,
        "score": score,
        "repo": repo,
        "dimensions": dimensions,
        "card_path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "gap": sections.get("gap", "Not captured."),
        "why_host_wont": sections.get("why host won't", "Not captured."),
        "product_angle": sections.get("product angle", "Not captured."),
        "competition": sections.get("competition / workarounds", "Not captured."),
        "kill_if": sections.get("kill if", "Not captured."),
        "tick_note": sections.get("tick note", ""),
        "decision": decision,
    }


def _slugify(text: str, max_len: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].rstrip("-")


def _load_state() -> dict:
    if not STATE_PATH.exists():
        return {"sent_sources": [], "updated_at": None}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def _save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def _load_top_cards() -> list[dict]:
    cards = []
    for path in CARDS_DIR.glob("*.md"):
        if path.name == ".gitkeep":
            continue
        card = _parse_card(path)
        if card:
            cards.append(card)
    cards.sort(key=lambda c: c["score"], reverse=True)
    return cards[:TOP_N]


def compute_payload() -> dict:
    state = _load_state()
    top_cards = _load_top_cards()
    sent_sources = set(state.get("sent_sources", []))
    unsent_top_cards = [c for c in top_cards if c["source"] not in sent_sources]
    for card in top_cards:
        card_slug = _slugify(card.get("title", "idea"))
        demo_rel = f"demos/top-ideas/{card_slug}/index.html"
        card["demo_path"] = demo_rel
        card["stackblitz_url"] = (
            f"https://stackblitz.com/fork/github/{GITHUB_REPO}"
            f"?file={demo_rel}&view=preview"
        )
        card["github_demo_url"] = (
            f"https://github.com/{GITHUB_REPO}/blob/{GITHUB_BRANCH}/{demo_rel}"
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "top_cards": top_cards,
        "unsent_top_cards": unsent_top_cards,
        "sent_count": len(sent_sources),
        "state_path": str(STATE_PATH),
    }


def _dimensions_to_summary(dimensions: str) -> str:
    if not dimensions:
        return "No dimension breakdown."
    pairs = re.findall(r"([a-z-]+)=(\d+)", dimensions)
    if not pairs:
        return dimensions
    label_map = {
        "standalone": "standalone",
        "wtp": "willingness-to-pay",
        "host-risk": "host-displacement risk",
        "solo-ship": "solo-shippability",
        "distribution": "distribution ease",
    }
    chunks = []
    for key, value in pairs:
        name = label_map.get(key, key)
        chunks.append(f"{name}: {value}/2")
    return ", ".join(chunks)

def _escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _generate_flow_steps(card: dict) -> list[str]:
    # Heuristic based on repo/title keywords. This is "demo flow", not actual product logic.
    t = (card.get("title") or "").lower()
    repo = (card.get("repo") or "").lower()

    if "git" in t and "sync" in t:
        return [
            "Connect: authenticate to your Git provider and choose collections format(s).",
            "Export: read collections from your API client(s) and write them into Git as files.",
            "Sync: watch for local changes, detect diffs, and push/pull with conflict-aware merge hints.",
            "Deploy: optionally open a PR or run a post-sync hook to update environments.",
        ]
    if "backup" in t or "restore" in t:
        return [
            "Connect: point to Coolify (or your PaaS) + pick storage (S3/R2) + encryption settings.",
            "Schedule: define backup windows and retention policies with one UI page.",
            "Run: trigger backups and run lightweight restore drills on a schedule.",
            "Verify: alert with status (success/failure) and provide a one-click restore path.",
        ]
    if "dmarc" in t:
        return [
            "Ingest: receive DMARC rua aggregate reports (mailbox/API import).",
            "Parse: extract per-domain pass/fail and source metadata into normalized tables.",
            "Dashboard: show trends and “top offenders” with plain-English explanations.",
            "Export: provide a weekly summary for admins (and optionally per-domain drill-down).",
        ]
    if "row level" in t or "rls" in t:
        return [
            "Input: paste Postgres RLS policy + add example roles/JWT claims.",
            "Compile: validate syntax and build an evaluation matrix.",
            "Test: run allow/deny decisions across sample requests and highlight failing predicates.",
            "Iterate: tweak policies and re-run until you get the expected access behavior.",
        ]

    # Fallback generic flow.
    return [
        "Setup: enter configuration/data required to reproduce the problem.",
        "Run: execute the core analysis step that answers “what happens?”.",
        "Explain: show why (not just what), with actionable next actions.",
        "Repeat: iterate quickly and track improvements across runs.",
    ]


def _generate_mvp_single_file_html(card: dict) -> str:
    title = card.get("title") or "Idea"
    source = card.get("source") or ""
    score = card.get("score") or ""
    gap = card.get("gap") or ""
    why_host = card.get("why_host_wont") or ""
    product_angle = card.get("product_angle") or ""
    competition = card.get("competition") or ""
    kill_if = card.get("kill_if") or ""
    tick_note = card.get("tick_note") or ""

    flow_steps = _generate_flow_steps(card)
    flow_steps_html = "\n".join(
        f"<li><span class='step'>{i}.</span> { _escape_html(s) }</li>"
        for i, s in enumerate(flow_steps, start=1)
    )

    # This is a "show to investors" lightweight static MVP:
    # one page, with tabs + demo interactions (client-side only).
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{_escape_html(title)} - Demo MVP</title>
    <style>
      :root {{
        --bg: #0b1220;
        --card: rgba(255,255,255,.06);
        --text: rgba(255,255,255,.92);
        --muted: rgba(255,255,255,.68);
        --accent: #60a5fa;
        --border: rgba(255,255,255,.12);
      }}
      body {{
        margin: 0;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji";
        background: linear-gradient(180deg, #0b1220, #070b14);
        color: var(--text);
      }}
      header {{
        padding: 28px 18px 18px;
        max-width: 1000px;
        margin: 0 auto;
      }}
      .badge {{
        display: inline-flex;
        gap: 8px;
        align-items: center;
        padding: 8px 12px;
        border: 1px solid var(--border);
        background: var(--card);
        border-radius: 999px;
        color: var(--muted);
        font-size: 13px;
      }}
      h1 {{
        margin: 14px 0 8px;
        font-size: 28px;
        line-height: 1.15;
      }}
      .subtitle {{
        color: var(--muted);
        max-width: 74ch;
        font-size: 15px;
      }}
      main {{
        max-width: 1000px;
        margin: 0 auto;
        padding: 14px 18px 36px;
      }}
      .grid {{
        display: grid;
        grid-template-columns: 1.1fr .9fr;
        gap: 16px;
      }}
      @media (max-width: 920px) {{ .grid {{ grid-template-columns: 1fr; }} }}
      .card {{
        border: 1px solid var(--border);
        background: var(--card);
        border-radius: 16px;
        padding: 16px;
      }}
      .tabs {{
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 12px;
      }}
      button.tab {{
        appearance: none;
        border: 1px solid var(--border);
        background: transparent;
        color: var(--muted);
        padding: 10px 12px;
        border-radius: 12px;
        cursor: pointer;
        font-weight: 600;
        font-size: 13px;
      }}
      button.tab[aria-selected="true"] {{
        border-color: rgba(96,165,250,.6);
        color: var(--text);
        background: rgba(96,165,250,.12);
      }}
      .panel {{ display: none; }}
      .panel[aria-hidden="false"] {{ display: block; }}
      h2 {{
        margin: 0 0 10px;
        font-size: 16px;
        letter-spacing: .2px;
      }}
      .muted {{ color: var(--muted); }}
      .list {{
        margin: 0;
        padding: 0;
        list-style: none;
      }}
      .list li {{
        padding: 10px 0;
        border-bottom: 1px dashed rgba(255,255,255,.14);
      }}
      .list li:last-child {{ border-bottom: none; }}
      .step {{
        display: inline-block;
        width: 28px;
        color: var(--accent);
        font-weight: 800;
      }}
      .code {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        font-size: 12.5px;
        background: rgba(0,0,0,.25);
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 12px;
        padding: 12px;
        overflow: auto;
        white-space: pre;
      }}
      .cta {{
        margin-top: 14px;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
      }}
      a.cta {{
        color: var(--text);
        text-decoration: none;
      }}
      .btn {{
        border: 1px solid rgba(96,165,250,.7);
        background: rgba(96,165,250,.15);
        padding: 10px 12px;
        border-radius: 12px;
        cursor: pointer;
        font-weight: 700;
        color: var(--text);
        transition: transform .05s ease-in-out;
      }}
      .btn:active {{ transform: translateY(1px); }}
      textarea {{
        width: 100%;
        min-height: 120px;
        background: rgba(0,0,0,.2);
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 12px;
        color: var(--text);
        padding: 12px;
        resize: vertical;
      }}
      .result {{
        margin-top: 12px;
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 12px;
        padding: 12px;
        background: rgba(0,0,0,.15);
      }}
      .small {{ font-size: 12.5px; color: var(--muted); line-height: 1.45; }}
    </style>
  </head>
  <body>
    <header>
      <div class="badge">
        <strong style="color: var(--text);">Demo MVP</strong>
        <span>Score: <strong style="color: var(--text);">{_escape_html(str(score))}/10</strong></span>
        <span class="muted">Source: <a href="{_escape_html(source)}" target="_blank" rel="noreferrer" style="color: var(--accent);">{_escape_html(source)}</a></span>
      </div>
      <h1>{_escape_html(title)}</h1>
      <div class="subtitle">
        A one-page investor demo showing the problem, the wedge, and the user flow.
        This file is client-only (no backend) so it’s safe to open anywhere.
      </div>
    </header>

    <main>
      <div class="grid">
        <section class="card">
          <div class="tabs" role="tablist" aria-label="Demo tabs">
            <button class="tab" role="tab" aria-selected="true" data-panel="landing">Landing</button>
            <button class="tab" role="tab" aria-selected="false" data-panel="problem">Problem</button>
            <button class="tab" role="tab" aria-selected="false" data-panel="solution">Solution</button>
            <button class="tab" role="tab" aria-selected="false" data-panel="flow">Flow</button>
          </div>

          <div class="panel" id="panel-landing" aria-hidden="false">
            <h2>Why this matters</h2>
            <div class="small">{_escape_html(gap)}</div>
            <div class="cta">
              <button class="btn" id="btnRunDemo">Run a quick demo</button>
              <button class="btn" id="btnReset">Reset</button>
            </div>
            <div class="result" id="demoResult" style="display:none;">
              <div style="font-weight:800; margin-bottom:6px;">Demo output (mock)</div>
              <div class="small" id="demoOutput"></div>
            </div>
            <div class="small" style="margin-top:10px;">
              { _escape_html("Investor note:") } { _escape_html(tick_note) if tick_note else _escape_html("No revalidation note captured in this card yet.") }
            </div>
          </div>

          <div class="panel" id="panel-problem" aria-hidden="true">
            <h2>Problem statement</h2>
            <div class="small"><strong>Gap:</strong> { _escape_html(gap) }</div>
            <div class="small" style="margin-top:10px;"><strong>Why host won’t:</strong> { _escape_html(why_host) }</div>
          </div>

          <div class="panel" id="panel-solution" aria-hidden="true">
            <h2>Solution (MVP wedge)</h2>
            <div class="small">{_escape_html(product_angle)}</div>
            <div class="small" style="margin-top:10px;"><strong>Competition / workarounds:</strong> { _escape_html(competition) }</div>
            <div class="small" style="margin-top:10px;"><strong>Kill criteria:</strong> { _escape_html(kill_if) }</div>
          </div>

          <div class="panel" id="panel-flow" aria-hidden="true">
            <h2>Flow(s)</h2>
            <ul class="list">
              {flow_steps_html}
            </ul>
          </div>
        </section>

        <aside class="card">
          <h2>Investor-friendly pitch snippet</h2>
          <div class="small" style="white-space: pre-line;">
            <strong>Wedge:</strong> {_escape_html(gap)}\n
            <strong>Moat:</strong> { _escape_html("We ship the workflow end-to-end: input -> run -> explain -> iterate, with fast onboarding.") }\n
            <strong>First customer demo:</strong> { _escape_html("Start with manual concierge for 1 week, then productize the repeatable core loop.") }\n
          </div>
          <div style="height: 12px;"></div>
          <h2>One-file HTML</h2>
          <div class="small muted">
            Open this file, then switch tabs to show: Landing → Problem → Solution → Flow.
            You can also copy the flow list into a slide.
          </div>
          <div style="height: 12px;"></div>
          <div class="code" aria-label="Copy/paste MVP">
{_escape_html("""// This MVP is already running in your browser as a static demo.
// Tip: take screenshots for an investor memo.
// Next: replace the mock demo output with real client-side parsing.
""")}
          </div>
        </aside>
      </div>
    </main>

    <script>
      const panels = Array.from(document.querySelectorAll('.panel'));
      const tabs = Array.from(document.querySelectorAll('button.tab'));
      function setPanel(id) {{
        for (const p of panels) {{
          const visible = p.id === 'panel-' + id;
          p.setAttribute('aria-hidden', visible ? 'false' : 'true');
        }}
        for (const t of tabs) {{
          const selected = t.getAttribute('data-panel') === id;
          t.setAttribute('aria-selected', selected ? 'true' : 'false');
        }}
      }}
      for (const tab of tabs) {{
        tab.addEventListener('click', () => setPanel(tab.dataset.panel));
      }}
      // Tiny "run demo" interaction (mock). Keeps investors engaged without backend.
      const btn = document.getElementById('btnRunDemo');
      const reset = document.getElementById('btnReset');
      const result = document.getElementById('demoResult');
      const output = document.getElementById('demoOutput');
      btn.addEventListener('click', () => {{
        result.style.display = 'block';
        output.textContent =
          "Demo created: user inputs setup data → the MVP shows an explanation-ready output (mock) → the user can iterate quickly.\\n" +
          "What investors want to see: the workflow is real, not just a feature list.";
      }});
      reset.addEventListener('click', () => {{
        result.style.display = 'none';
        output.textContent = '';
      }});
    </script>
  </body>
</html>"""


def _generate_mvp_snippet_html(card: dict) -> str:
    # Compact HTML meant for email (small enough to be included in-message).
    title = card.get("title") or "Idea"
    gap = card.get("gap") or ""
    why_host = card.get("why_host_wont") or ""
    product_angle = card.get("product_angle") or ""
    competition = card.get("competition") or ""
    kill_if = card.get("kill_if") or ""
    source = card.get("source") or ""

    flow_steps = _generate_flow_steps(card)
    flow_items = "\n".join(f"<li><strong>{i}.</strong> {_escape_html(s)}</li>" for i, s in enumerate(flow_steps, start=1))

    return f"""<!doctype html>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{_escape_html(title)} - MVP</title>
<style>
  body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 24px; line-height: 1.5; }}
  .row {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 14px; }}
  button {{ cursor: pointer; padding: 10px 12px; border: 1px solid #ddd; background: #fff; border-radius: 10px; }}
  .panel {{ display: none; border: 1px solid #eee; border-radius: 14px; padding: 14px; }}
  .panel.active {{ display: block; }}
  .muted {{ color: #555; }}
  ul {{ padding-left: 18px; }}
  pre {{ white-space: pre-wrap; background: #111; color: #fff; padding: 12px; border-radius: 12px; overflow:auto; }}
</style>
<div class="row">
  <button onclick="show('landing')">Landing</button>
  <button onclick="show('problem')">Problem</button>
  <button onclick="show('solution')">Solution</button>
  <button onclick="show('flow')">Flow</button>
</div>

<h1>{_escape_html(title)}</h1>
<div class="muted">Source: <a href="{_escape_html(source)}">{_escape_html(source)}</a></div>

<div id="panel-landing" class="panel active">
  <h2>Landing</h2>
  <p>{_escape_html(gap)}</p>
</div>

<div id="panel-problem" class="panel">
  <h2>Problem</h2>
  <p><strong>Gap:</strong> {_escape_html(gap)}</p>
  <p><strong>Why host won’t:</strong> {_escape_html(why_host)}</p>
</div>

<div id="panel-solution" class="panel">
  <h2>Solution (MVP wedge)</h2>
  <p>{_escape_html(product_angle)}</p>
  <p><strong>Competition/workarounds:</strong> {_escape_html(competition)}</p>
  <p><strong>Kill criteria:</strong> {_escape_html(kill_if)}</p>
</div>

<div id="panel-flow" class="panel">
  <h2>Flow(s)</h2>
  <ul>{flow_items}</ul>
</div>

<script>
  function show(id) {{
    for (const p of document.querySelectorAll('.panel')) p.classList.remove('active');
    document.getElementById('panel-' + id).classList.add('active');
  }}
</script>
"""


def generate_demo_files(cards: list[dict]) -> list[str]:
    generated: list[str] = []
    for card in cards:
        card_slug = _slugify(card.get("title", "idea"))
        demo_dir = DEMOS_DIR / card_slug
        demo_dir.mkdir(parents=True, exist_ok=True)
        demo_file = demo_dir / "index.html"
        demo_file.write_text(_generate_mvp_single_file_html(card), encoding="utf-8")
        generated.append(str(demo_file.relative_to(ROOT)).replace("\\", "/"))
    return generated


def render_email_text(cards: list[dict], generated_at: str) -> str:
    lines: list[str] = []
    lines.append("Idea Harvester - Decision Brief")
    lines.append("")
    lines.append(
        "This digest is designed to help you decide what to pursue, not just list ideas."
    )
    lines.append(f"Generated: {generated_at}")
    lines.append("")
    for idx, card in enumerate(cards, start=1):
        lines.append(f"{idx}) {card['title']} ({card['score']}/10) - {card['decision']}")
        lines.append(f"Repo signal: {card.get('repo') or 'n/a'}")
        lines.append(f"Source: {card['source']}")
        lines.append(f"What it is: {card['gap']}")
        lines.append(f"Why this can exist now: {card['why_host_wont']}")
        lines.append(f"How you'd build/sell first: {card['product_angle']}")
        lines.append(f"Competition/workarounds: {card['competition']}")
        lines.append(f"What would kill it: {card['kill_if']}")
        lines.append(
            f"Rubric breakdown: {_dimensions_to_summary(card.get('dimensions', ''))}"
        )
        if card.get("tick_note"):
            lines.append(f"Latest revalidation note: {card['tick_note']}")
        lines.append("")

    lines.append("How to use this:")
    lines.append("- Pick 1 idea only.")
    lines.append("- Run 3 design-partner calls in 7 days.")
    lines.append("- If fewer than 3 strong yeses, move to the next idea.")
    return "\n".join(lines)


def render_email_html(cards: list[dict], generated_at: str) -> str:
    def card_block(card: dict, idx: int) -> str:
        title = _escape_html(card.get("title", ""))
        repo = _escape_html(card.get("repo", "") or "n/a")
        source = _escape_html(card.get("source", ""))
        decision = _escape_html(card.get("decision", ""))
        score = _escape_html(str(card.get("score", "")))

        mvp_html = _generate_mvp_snippet_html(card)
        mvp_html_escaped = _escape_html(mvp_html)

        tick_note = card.get("tick_note", "").strip()
        tick_note_html = (
            f"<div style='margin-top:8px;'><strong>Latest revalidation note:</strong> {_escape_html(tick_note)}</div>"
            if tick_note
            else ""
        )

        return f"""
<div style="border:1px solid rgba(0,0,0,.12); background: #f7f7f7; border-radius:16px; padding:16px; margin:16px 0;">
  <div style="font-weight:900; font-size:16px;">
    {idx}) {title} ({score}/10) - {decision}
  </div>
  <div style="color: rgba(0,0,0,.55); margin-top:6px; font-size:13px;">
    Repo signal: {repo}
  </div>
  <div style="margin-top:8px; font-size:13px;">
    Source: <a href="{source}" target="_blank" rel="noreferrer">{source}</a>
  </div>
  <div style="margin-top:8px; font-size:13px;">
    Demo:
    <a href="{_escape_html(card.get('stackblitz_url', ''))}" target="_blank" rel="noreferrer">Open in StackBlitz</a>
    ·
    <a href="{_escape_html(card.get('github_demo_url', ''))}" target="_blank" rel="noreferrer">View HTML on GitHub</a>
  </div>

  <div style="margin-top:12px; font-size:13.5px; color: #111;">
    <div><strong>What it is:</strong> {_escape_html(card.get("gap", ""))}</div>
    <div style="margin-top:8px;"><strong>Why this can exist now:</strong> {_escape_html(card.get("why_host_wont", ""))}</div>
    <div style="margin-top:8px;"><strong>How you'd build/sell first:</strong> {_escape_html(card.get("product_angle", ""))}</div>
    <div style="margin-top:8px;"><strong>Competition/workarounds:</strong> {_escape_html(card.get("competition", ""))}</div>
    <div style="margin-top:8px;"><strong>What would kill it:</strong> {_escape_html(card.get("kill_if", ""))}</div>
    {tick_note_html}
  </div>

  <details style="margin-top:12px;">
    <summary style="cursor:pointer; font-weight:800;">Investor demo: single-file HTML (copy/paste)</summary>
    <div style="margin-top:10px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; font-size:12.5px; background: #111; color:#fff; border-radius:12px; padding:12px; white-space: pre; overflow:auto;">
{mvp_html_escaped}
    </div>
  </details>

  <div style="margin-top:10px; color: rgba(0,0,0,.55); font-size:12.5px;">
    StackBlitz direct open links require a shared template repo (I can add real links after you approve creating it).
  </div>
</div>
"""

    parts: list[str] = []
    parts.append("<div style='font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; color: #111;'>")
    parts.append("<h2 style='margin:0 0 8px;'>Idea Harvester - Decision Brief (with Investor MVP HTML)</h2>")
    parts.append(f"<div style='color:#444; font-size:14px; margin-bottom:16px;'>Generated: {_escape_html(generated_at)}</div>")
    parts.append("<div style='color:#444; font-size:14px; margin-bottom:10px;'>Each idea includes a one-file HTML investor demo (landing, problem, solution, flow).</div>")
    for idx, card in enumerate(cards, start=1):
        parts.append(card_block(card, idx))

    parts.append("<h3 style='margin:18px 0 6px;'>Decision path</h3>")
    parts.append("<ol style='margin:0; padding-left:18px; color:#333;'>")
    parts.append("<li>Pick 1 idea only.</li>")
    parts.append("<li>Run 3 design-partner calls in 7 days.</li>")
    parts.append("<li>If fewer than 3 strong yeses, move to the next idea.</li>")
    parts.append("</ol>")
    parts.append("</div>")
    return "\n".join(parts)


def mark_current_top_sent() -> dict:
    payload = compute_payload()
    state = _load_state()
    sent_sources = set(state.get("sent_sources", []))
    for card in payload["unsent_top_cards"]:
        sent_sources.add(card["source"])
    state["sent_sources"] = sorted(sent_sources)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_state(state)
    return compute_payload()


def main() -> None:
    import sys

    if "--mark-current-sent" in sys.argv:
        result = mark_current_top_sent()
    elif "--generate-demos" in sys.argv:
        payload = compute_payload()
        generated = generate_demo_files(payload["top_cards"])
        print(json.dumps({"generated": generated, "count": len(generated)}, indent=2))
        return
    elif "--email-text" in sys.argv:
        payload = compute_payload()
        only_unsent = "--unsent-only" in sys.argv
        cards = payload["unsent_top_cards"] if only_unsent else payload["top_cards"]
        print(render_email_text(cards, payload["generated_at"]))
        return
    elif "--email-html" in sys.argv:
        payload = compute_payload()
        only_unsent = "--unsent-only" in sys.argv
        cards = payload["unsent_top_cards"] if only_unsent else payload["top_cards"]
        print(render_email_html(cards, payload["generated_at"]))
        return
    else:
        result = compute_payload()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
