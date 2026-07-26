#!/usr/bin/env bash
# Single keep-going harvest wake. Do not put the sentinel string in argv
# of a parent that also runs pkill -f on that string (self-kill).
set -euo pipefail
INTERVAL="${HARVEST_LOOP_INTERVAL:-1800}"
while true; do
  sleep "$INTERVAL"
  echo 'AGENT_LOOP_TICK_harvest {"prompt":"Read LOOP.md + CONTROLLER.json. Run one harvest tick: harvest.py > candidates.md; score status:new with RUBRIC.md into cards/ or killed/; gc_cards.py; if zero new then expand sources or boards research and re-harvest; update CONTROLLER.json; commit; git push origin HEAD. Do not ask human. Never start a second loop."}'
done
