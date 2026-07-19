$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    throw "Python environment not found. Run .\setup.ps1 first."
}

& ".\.venv\Scripts\python.exe" ".\scripts\generate_posts.py" --config ".\config.json"
