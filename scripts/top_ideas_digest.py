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
        demo_folder_rel = f"demos/top-ideas/{card_slug}"
        card["demo_path"] = demo_rel
        card["demo_folder"] = demo_folder_rel
        card["stackblitz_url"] = (
            f"https://stackblitz.com/github/{GITHUB_REPO}/tree/{GITHUB_BRANCH}/{demo_folder_rel}"
            f"?file=index.html&view=preview&startScript=start"
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


def _infer_demo_mode(card: dict) -> str:
    title = (card.get("title") or "").lower()
    if "git" in title and "sync" in title:
        return "git_sync"
    if "backup" in title or "restore" in title:
        return "backup_restore"
    if "dmarc" in title:
        return "dmarc"
    if "row level" in title or "rls" in title:
        return "rls"
    return "generic"


def _mvp_module_html(mode: str) -> str:
    if mode == "git_sync":
        return """
<section class="panel active" id="panel-demo">
  <h2>Demo Lab: Multi-client collection sync</h2>
  <p class="muted">Load two client exports, detect conflicts, generate merge output and PR summary.</p>
  <div class="two">
    <div>
      <label>Client A export (JSON)</label>
      <textarea id="aData">{ "endpoints": ["GET /users", "POST /login", "GET /orders"] }</textarea>
    </div>
    <div>
      <label>Client B export (JSON)</label>
      <textarea id="bData">{ "endpoints": ["GET /users", "POST /auth/login", "GET /orders", "DELETE /orders/:id"] }</textarea>
    </div>
  </div>
  <div class="row">
    <button onclick="runGitAnalysis()">Analyze diff</button>
    <button onclick="acceptA()">Prefer A for conflicts</button>
    <button onclick="acceptB()">Prefer B for conflicts</button>
  </div>
  <div class="result" id="gitResult"></div>
</section>
"""
    if mode == "backup_restore":
        return """
<section class="panel active" id="panel-demo">
  <h2>Demo Lab: Backup scheduler + restore drill</h2>
  <p class="muted">Configure retention and run a restore drill with measured RTO.</p>
  <div class="two">
    <div>
      <label>App</label>
      <input id="appName" value="coolify-prod" />
      <label>Target storage</label>
      <input id="storage" value="s3://company-backups/coolify" />
      <label>Retention days</label>
      <input id="retention" type="number" value="14" />
    </div>
    <div>
      <label>Schedule</label>
      <input id="schedule" value="0 */6 * * *" />
      <label>Encryption key ID</label>
      <input id="kmsKey" value="kms-prod-01" />
      <label>RTO target (minutes)</label>
      <input id="rto" type="number" value="20" />
    </div>
  </div>
  <div class="row">
    <button onclick="planBackup()">Plan backup policy</button>
    <button onclick="runDrill()">Run restore drill</button>
  </div>
  <div class="result" id="backupResult"></div>
</section>
"""
    if mode == "dmarc":
        return """
<section class="panel active" id="panel-demo">
  <h2>Demo Lab: DMARC report parser</h2>
  <p class="muted">Paste aggregate XML and get pass/fail breakdown and risk signal.</p>
  <label>Aggregate XML</label>
  <textarea id="xmlData"><feedback><record><row><source_ip>1.2.3.4</source_ip><count>120</count><policy_evaluated><dkim>pass</dkim><spf>fail</spf></policy_evaluated></row></record><record><row><source_ip>5.6.7.8</source_ip><count>42</count><policy_evaluated><dkim>fail</dkim><spf>fail</spf></policy_evaluated></row></record></feedback></textarea>
  <div class="row">
    <button onclick="parseDmarc()">Parse report</button>
  </div>
  <div class="result" id="dmarcResult"></div>
</section>
"""
    if mode == "rls":
        return """
<section class="panel active" id="panel-demo">
  <h2>Demo Lab: RLS policy tester</h2>
  <p class="muted">Test role/JWT scenarios and explain allow/deny decisions.</p>
  <label>Policy rules (pseudo)</label>
  <textarea id="policyData">allow select when role in [admin,manager]
allow update when role=member and owner_id = jwt.sub
deny delete when role=member</textarea>
  <label>Test cases (JSON)</label>
  <textarea id="casesData">[
  {"action":"select","role":"member","owner_id":"u1","jwt_sub":"u1"},
  {"action":"update","role":"member","owner_id":"u2","jwt_sub":"u1"},
  {"action":"update","role":"member","owner_id":"u1","jwt_sub":"u1"},
  {"action":"delete","role":"admin","owner_id":"u1","jwt_sub":"u1"}
]</textarea>
  <div class="row">
    <button onclick="runRlsTests()">Run tests</button>
  </div>
  <div class="result" id="rlsResult"></div>
</section>
"""
    return """
<section class="panel active" id="panel-demo">
  <h2>Demo Lab</h2>
  <p class="muted">Generic MVP simulation for this idea.</p>
  <textarea id="genericInput">Describe your input scenario...</textarea>
  <div class="row"><button onclick="runGeneric()">Run</button></div>
  <div class="result" id="genericResult"></div>
</section>
"""


# Override with a richer, problem-specific MVP generator.
def _generate_mvp_single_file_html(card: dict) -> str:
    mode = _infer_demo_mode(card)
    title = card.get("title") or "Idea"
    source = card.get("source") or ""
    gap = card.get("gap") or ""
    why_host = card.get("why_host_wont") or ""
    product_angle = card.get("product_angle") or ""
    competition = card.get("competition") or ""
    kill_if = card.get("kill_if") or ""
    decision = card.get("decision") or "PURSUE"
    score = card.get("score") or "?"
    flow_steps = _generate_flow_steps(card)
    flow_html = "".join(f"<li>{_escape_html(step)}</li>" for step in flow_steps)
    module_html = _mvp_module_html(mode)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_escape_html(title)} - MVP</title>
  <style>
    :root {{ --fg:#0f172a; --muted:#475569; --line:#e2e8f0; --bg:#f8fafc; --card:#ffffff; --accent:#2563eb; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial; color:var(--fg); background:var(--bg); }}
    .wrap {{ max-width:1100px; margin:0 auto; padding:20px; }}
    .hero {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px; }}
    .kpis {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin-top:12px; }}
    .kpi {{ border:1px solid var(--line); border-radius:12px; padding:10px; background:#fff; }}
    .kpi .label {{ color:var(--muted); font-size:12px; }}
    .kpi .val {{ font-weight:700; margin-top:4px; }}
    .layout {{ display:grid; grid-template-columns:2fr 1fr; gap:14px; margin-top:14px; }}
    .card {{ background:#fff; border:1px solid var(--line); border-radius:14px; padding:14px; }}
    .tabs {{ display:flex; gap:8px; margin-bottom:12px; flex-wrap:wrap; }}
    button {{ border:1px solid var(--line); background:#fff; border-radius:10px; padding:9px 11px; cursor:pointer; }}
    button.primary {{ border-color:#93c5fd; background:#eff6ff; color:#1d4ed8; }}
    .muted {{ color:var(--muted); font-size:13px; }}
    textarea, input {{ width:100%; border:1px solid var(--line); border-radius:10px; padding:10px; font:inherit; }}
    textarea {{ min-height:110px; }}
    .row {{ display:flex; gap:8px; margin-top:10px; flex-wrap:wrap; }}
    .two {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; }}
    .result {{ margin-top:10px; border:1px solid var(--line); border-radius:10px; background:#f8fafc; padding:10px; white-space:pre-wrap; font-size:13px; }}
    ul {{ margin:6px 0 0; padding-left:18px; }}
    @media (max-width:900px) {{ .layout {{ grid-template-columns:1fr; }} .kpis {{ grid-template-columns:1fr 1fr; }} .two {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <h1 style="margin:0 0 6px;">{_escape_html(title)}</h1>
      <div class="muted">Source: <a href="{_escape_html(source)}" target="_blank" rel="noreferrer">{_escape_html(source)}</a></div>
      <div class="kpis">
        <div class="kpi"><div class="label">Decision</div><div class="val">{_escape_html(str(decision))}</div></div>
        <div class="kpi"><div class="label">Score</div><div class="val">{_escape_html(str(score))}/10</div></div>
        <div class="kpi"><div class="label">Primary wedge</div><div class="val">{_escape_html(gap[:56] + ("..." if len(gap) > 56 else ""))}</div></div>
        <div class="kpi"><div class="label">First risk</div><div class="val">{_escape_html(kill_if[:56] + ("..." if len(kill_if) > 56 else ""))}</div></div>
      </div>
    </div>

    <div class="layout">
      <div class="card">
        <div class="tabs">
          <button class="primary" onclick="show('demo')">Demo Lab</button>
          <button onclick="show('problem')">Problem</button>
          <button onclick="show('solution')">Solution</button>
          <button onclick="show('flows')">Flow(s)</button>
        </div>

        {module_html}

        <section class="panel" id="panel-problem" style="display:none;">
          <h2>Problem</h2>
          <p>{_escape_html(gap)}</p>
          <h3>Why now</h3>
          <p>{_escape_html(why_host)}</p>
        </section>

        <section class="panel" id="panel-solution" style="display:none;">
          <h2>Solution MVP</h2>
          <p>{_escape_html(product_angle)}</p>
          <h3>Competition/workarounds</h3>
          <p>{_escape_html(competition)}</p>
          <h3>Kill condition</h3>
          <p>{_escape_html(kill_if)}</p>
        </section>

        <section class="panel" id="panel-flows" style="display:none;">
          <h2>Flow(s)</h2>
          <ul>{flow_html}</ul>
        </section>
      </div>

      <div class="card">
        <h2 style="margin-top:0;">Investor one-minute read</h2>
        <p class="muted">What this demo proves:</p>
        <ul>
          <li>The user workflow is concrete, not just an idea statement.</li>
          <li>The MVP has a clear first-user path and output artifact.</li>
          <li>Main risk is explicit and measurable in early tests.</li>
        </ul>
        <h3>Pilot success criteria</h3>
        <ul>
          <li>3 design partners run the workflow end to end.</li>
          <li>At least 1 team repeats weekly in the first 14 days.</li>
          <li>At least 1 asks for a paid/hosted continuation.</li>
        </ul>
      </div>
    </div>
  </div>

  <script>
    function show(name) {{
      for (const p of document.querySelectorAll('.panel')) p.style.display = 'none';
      document.getElementById('panel-' + name).style.display = 'block';
    }}

    function runGitAnalysis() {{
      try {{
        const a = JSON.parse(document.getElementById('aData').value);
        const b = JSON.parse(document.getElementById('bData').value);
        const sa = new Set(a.endpoints || []);
        const sb = new Set(b.endpoints || []);
        const onlyA = [...sa].filter(x => !sb.has(x));
        const onlyB = [...sb].filter(x => !sa.has(x));
        const both = [...sa].filter(x => sb.has(x));
        const out = [
          'Shared endpoints: ' + both.length,
          'Only in A: ' + (onlyA.join(', ') || 'none'),
          'Only in B: ' + (onlyB.join(', ') || 'none'),
          '',
          'PR summary:',
          '- add ' + onlyB.length + ' endpoint(s)',
          '- keep ' + both.length + ' endpoint(s)',
          '- review rename candidates from A to B'
        ].join('\\n');
        document.getElementById('gitResult').textContent = out;
      }} catch (e) {{
        document.getElementById('gitResult').textContent = 'Invalid JSON input.';
      }}
    }}
    function acceptA() {{ document.getElementById('gitResult').textContent += '\\nResolution: preferred Client A names.'; }}
    function acceptB() {{ document.getElementById('gitResult').textContent += '\\nResolution: preferred Client B names.'; }}

    function planBackup() {{
      const app = document.getElementById('appName').value;
      const storage = document.getElementById('storage').value;
      const schedule = document.getElementById('schedule').value;
      const retention = document.getElementById('retention').value;
      document.getElementById('backupResult').textContent =
        'Policy created\\n' +
        '- App: ' + app + '\\n' +
        '- Storage: ' + storage + '\\n' +
        '- Schedule: ' + schedule + '\\n' +
        '- Retention: ' + retention + ' days';
    }}
    function runDrill() {{
      const target = Number(document.getElementById('rto').value || '20');
      const actual = Math.max(4, Math.round(target * (0.7 + Math.random() * 0.7)));
      const pass = actual <= target;
      document.getElementById('backupResult').textContent +=
        '\\n\\nRestore drill result\\n- target RTO: ' + target + 'm\\n- actual RTO: ' + actual + 'm\\n- status: ' + (pass ? 'PASS' : 'FAIL');
    }}

    function parseDmarc() {{
      const raw = document.getElementById('xmlData').value;
      try {{
        const doc = new DOMParser().parseFromString(raw, 'text/xml');
        const rows = [...doc.getElementsByTagName('record')];
        let total = 0, spfFail = 0, dkimFail = 0;
        const lines = [];
        for (const r of rows) {{
          const count = Number(r.getElementsByTagName('count')[0]?.textContent || '0');
          const ip = r.getElementsByTagName('source_ip')[0]?.textContent || 'n/a';
          const spf = (r.getElementsByTagName('spf')[0]?.textContent || '').toLowerCase();
          const dkim = (r.getElementsByTagName('dkim')[0]?.textContent || '').toLowerCase();
          total += count;
          if (spf === 'fail') spfFail += count;
          if (dkim === 'fail') dkimFail += count;
          lines.push(ip + ': count=' + count + ', spf=' + spf + ', dkim=' + dkim);
        }}
        const risk = (spfFail + dkimFail) / Math.max(total * 2, 1);
        document.getElementById('dmarcResult').textContent =
          'Records: ' + rows.length + '\\nTotal volume: ' + total +
          '\\nSPF fail volume: ' + spfFail +
          '\\nDKIM fail volume: ' + dkimFail +
          '\\nRisk score: ' + risk.toFixed(2) +
          '\\n\\nPer source:\\n' + lines.join('\\n');
      }} catch (e) {{
        document.getElementById('dmarcResult').textContent = 'Unable to parse XML.';
      }}
    }}

    function runRlsTests() {{
      const raw = document.getElementById('casesData').value;
      try {{
        const tests = JSON.parse(raw);
        const lines = [];
        let pass = 0;
        for (const t of tests) {{
          let allow = false;
          if (t.action === 'select' && ['admin','manager'].includes(t.role)) allow = true;
          if (t.action === 'update' && t.role === 'member' && t.owner_id === t.jwt_sub) allow = true;
          if (t.action === 'delete' && t.role === 'member') allow = false;
          const verdict = allow ? 'ALLOW' : 'DENY';
          if (allow) pass += 1;
          lines.push(t.action + ' as ' + t.role + ' -> ' + verdict);
        }}
        document.getElementById('rlsResult').textContent =
          'Evaluated: ' + tests.length + '\\nAllowed: ' + pass + '\\nDenied: ' + (tests.length - pass) + '\\n\\n' + lines.join('\\n');
      }} catch (e) {{
        document.getElementById('rlsResult').textContent = 'Invalid test cases JSON.';
      }}
    }}

    function runGeneric() {{
      const input = document.getElementById('genericInput').value || '';
      document.getElementById('genericResult').textContent =
        'Input accepted.\\nGenerated a problem-solution-flow preview for: ' + input.slice(0, 120);
    }}
  </script>
</body>
</html>"""


def generate_demo_files(cards: list[dict]) -> list[str]:
    generated: list[str] = []
    for card in cards:
        card_slug = _slugify(card.get("title", "idea"))
        demo_dir = DEMOS_DIR / card_slug
        demo_dir.mkdir(parents=True, exist_ok=True)
        demo_file = demo_dir / "index.html"
        demo_file.write_text(_generate_mvp_single_file_html(card), encoding="utf-8")
        package_file = demo_dir / "package.json"
        package_file.write_text(
            json.dumps(
                {
                    "name": f"idea-demo-{card_slug}",
                    "private": True,
                    "scripts": {
                        "start": "node -e \"const http=require('http');const fs=require('fs');const p=require('path');const root=process.cwd();const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.ico':'image/x-icon'};http.createServer((req,res)=>{let u=(req.url||'/').split('?')[0];if(u==='/'||u==='')u='/index.html';const f=p.join(root,decodeURIComponent(u));if(!f.startsWith(root)){res.writeHead(403);return res.end('forbidden');}fs.readFile(f,(e,d)=>{if(e){res.writeHead(404);return res.end('not found');}res.writeHead(200,{'Content-Type':mime[p.extname(f)]||'application/octet-stream'});res.end(d);});}).listen(4173,'0.0.0.0',()=>console.log('server at 4173'));\""
                    },
                    "stackblitz": {"startCommand": "npm run start"},
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
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

        return f"""
<div style="border:1px solid #e5e7eb; border-radius:12px; padding:12px; margin:10px 0;">
  <div style="font-weight:700; font-size:28px;">
    {idx}) {title}
  </div>
  <div style="font-size:13px; color:#374151; margin-top:4px;">
    Score: {score}/10 · {decision}
  </div>
  <div style="font-size:13px; color:#6b7280; margin-top:4px;">
    Repo signal: {repo}
  </div>
  <div style="font-size:13px; color:#6b7280; margin-top:4px;">
    Source: <a href="{source}" target="_blank" rel="noreferrer">{source}</a>
  </div>
  <div style="margin-top:8px;">
    <a href="{_escape_html(card.get('stackblitz_url', ''))}" target="_blank" rel="noreferrer">Open in StackBlitz</a>
    <span style="color:#9ca3af;"> · </span>
    <a href="{_escape_html(card.get('github_demo_url', ''))}" target="_blank" rel="noreferrer">View HTML on GitHub</a>
  </div>
  <div style="margin-top:10px; font-size:13px; color:#111827;">
    <div><strong>Idea:</strong> {_escape_html(card.get("gap", ""))}</div>
    <div style="margin-top:6px;"><strong>Why now:</strong> {_escape_html(card.get("why_host_wont", ""))}</div>
    <div style="margin-top:6px;"><strong>MVP:</strong> {_escape_html(card.get("product_angle", ""))}</div>
    <div style="margin-top:6px;"><strong>Risk:</strong> {_escape_html(card.get("kill_if", ""))}</div>
    <div style="margin-top:6px;"><strong>Flow:</strong> {_escape_html(" | ".join(_generate_flow_steps(card)))}</div>
  </div>
</div>
"""

    parts: list[str] = []
    parts.append("<div style='font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; color:#111;'>")
    parts.append("<h2 style='margin:0 0 8px;'>Idea Harvester: Demo MVPs for each top idea</h2>")
    parts.append(f"<div style='color:#4b5563; font-size:13px; margin-bottom:12px;'>Generated: {_escape_html(generated_at)}</div>")
    parts.append("<div style='color:#374151; margin-bottom:14px;'>Each idea includes <strong>Landing</strong>, <strong>Problem</strong>, <strong>Solution</strong>, and <strong>Flow</strong> plus decision context.</div>")
    for idx, card in enumerate(cards, start=1):
        parts.append(card_block(card, idx))
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
