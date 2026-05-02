$projectRoot = Split-Path -Parent $PSScriptRoot
$backendPath = Join-Path $projectRoot "backend"
$venvPython = Join-Path $backendPath ".venv\Scripts\python.exe"

Set-Location $backendPath
if (Test-Path $venvPython) {
    & $venvPython -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5062
}
else {
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5062
}
