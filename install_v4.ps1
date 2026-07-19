$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    throw "Existing virtual environment not found. Run .\setup.ps1 first."
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade json-repair

Write-Host ""
Write-Host "JSON repair dependency installed."
Write-Host "Now run: .\run_generator.ps1"
