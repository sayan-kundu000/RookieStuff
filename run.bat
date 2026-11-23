@echo off
cd /d "%~dp0"
echo Starting RookieStuff on port 3000...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 3000 --reload --reload-dir app
) else (
    python -m uvicorn main:app --host 0.0.0.0 --port 3000 --reload --reload-dir app
)
pause
