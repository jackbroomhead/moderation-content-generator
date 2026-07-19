param(
    [string]$PlanPath = ".\generation_plan_smoke_v4.json"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Output = Join-Path $Root "output"
$Logs = Join-Path $Output "automation-logs"
$Lock = Join-Path $Output "generation-run.lock"
$Runner = Join-Path $Root "run_generation_plan.ps1"
$ResolvedPlan = (Resolve-Path $PlanPath).Path

New-Item -ItemType Directory -Force -Path $Logs | Out-Null

if (Test-Path $Lock) {
    $Active = @(
        Get-CimInstance Win32_Process |
        Where-Object {
            $_.CommandLine -match "run_generation_plan\.ps1|run_generator\.ps1|generate_posts\.py"
        }
    )

    if ($Active.Count -gt 0) {
        Write-Host "A generation process is still active."
        $Active |
            Select-Object ProcessId, Name, CommandLine |
            Format-Table -AutoSize
        exit 2
    }

    Remove-Item $Lock -Force
    Write-Host "Removed stale generation lock left by the timed-out Hermes call."
}

$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$StdOut = Join-Path $Logs "background-$Stamp-stdout.log"
$StdErr = Join-Path $Logs "background-$Stamp-stderr.log"

$Arguments = @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-File", "`"$Runner`"",
    "-PlanPath", "`"$ResolvedPlan`""
)

$Process = Start-Process `
    -FilePath "powershell.exe" `
    -ArgumentList $Arguments `
    -WorkingDirectory $Root `
    -RedirectStandardOutput $StdOut `
    -RedirectStandardError $StdErr `
    -WindowStyle Hidden `
    -PassThru

[pscustomobject]@{
    state = "started"
    processId = $Process.Id
    plan = $ResolvedPlan
    stdout = $StdOut
    stderr = $StdErr
} | ConvertTo-Json -Depth 5
