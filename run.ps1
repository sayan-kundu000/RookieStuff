# PowerShell launch helper for RookieStuff
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "Starting RookieStuff on port 3000..." -ForegroundColor Green
$venvPython = Join-Path $ScriptDir ".venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    & $venvPython -m uvicorn main:app --host 0.0.0.0 --port 3000 --reload --reload-dir app
} else {
    python -m uvicorn main:app --host 0.0.0.0 --port 3000 --reload --reload-dir app
}
