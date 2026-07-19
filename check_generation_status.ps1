$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Output = Join-Path $Root "output"
$Logs = Join-Path $Output "automation-logs"
$Lock = Join-Path $Output "generation-run.lock"

$Progress = Get-ChildItem $Logs -Filter "generation-*-progress.json" -File `
    -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

$Summary = Get-ChildItem $Logs -Filter "generation-*-summary.txt" -File `
    -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

$Active = @(
    Get-CimInstance Win32_Process |
    Where-Object {
        $_.CommandLine -match "run_generation_plan\.ps1|run_generator\.ps1|generate_posts\.py"
    }
)

$State = if ($Active.Count -gt 0 -or (Test-Path $Lock)) {
    "running"
}
elseif ($Progress) {
    try {
        (Get-Content $Progress.FullName -Raw | ConvertFrom-Json).state
    }
    catch {
        "finished_unknown"
    }
}
else {
    "not_started"
}

Write-Host "State: $State"
Write-Host "Active generation processes: $($Active.Count)"
Write-Host "Lock exists: $(Test-Path $Lock)"

if ($Progress) {
    Write-Host "Progress: $($Progress.FullName)"
    Get-Content $Progress.FullName -Raw
}

if ($State -ne "running" -and $Summary) {
    Write-Host ""
    Write-Host "Latest summary: $($Summary.FullName)"
    Get-Content $Summary.FullName
}
