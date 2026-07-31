# Detached 30m harvest tick writer. Survives Cursor shell cleanup.
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$log = Join-Path $root '.harvest_tick.log'
$pidFile = Join-Path $root '.harvest_sentinel.pid'
$payload = 'AGENT_LOOP_TICK_harvest {"prompt":"Read LOOP.md + CONTROLLER.json. Run one harvest tick: harvest.py; harvest_boards.py; harvest_discourse.py; score status:new with RUBRIC.md into cards/ or killed/; gc_cards.py; if zero new then idle per LOOP; update CONTROLLER.json; commit; git push origin HEAD. Do not ask human. Never start a second loop."}'

[System.IO.File]::WriteAllText($pidFile, "$PID")
Add-Content -Path $log -Value ("{0} armed pid={1}" -f (Get-Date).ToString('o'), $PID)

while ($true) {
  Start-Sleep -Seconds 1800
  Add-Content -Path $log -Value $payload
}
