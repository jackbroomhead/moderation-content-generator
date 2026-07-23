param(
    [string]$TaskName = "Moderation Nightly Candidate Generation",
    [string]$At = "01:00",
    [int]$TotalPosts = 40,
    [string]$DaysCsv = "3,6,10,13",
    [int]$MaxRuntimeMinutes = 360,
    [int]$RetryAttemptsPerProfile = 4,
    [bool]$UnloadModelsOnFinish = $true,
    [string]$Label = "nightly"
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Runner = Join-Path $Root "run_nightly_generation.ps1"
if (-not (Test-Path -LiteralPath $Runner)) {
    throw "Missing nightly generation script: $Runner"
}

$User = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$UnloadFlagText = if ($UnloadModelsOnFinish) { '$true' } else { '$false' }
$Argument = (
    "-NoProfile -ExecutionPolicy Bypass -File `"$Runner`" " +
    "-TotalPosts $TotalPosts -DaysCsv `"$DaysCsv`" " +
    "-MaxRuntimeMinutes $MaxRuntimeMinutes -RetryAttemptsPerProfile $RetryAttemptsPerProfile " +
    "-UnloadModelsOnFinish $UnloadFlagText " +
    "-Label `"$Label`""
)

$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument $Argument `
    -WorkingDirectory $Root
$Trigger = New-ScheduledTaskTrigger -Daily -At $At
$Principal = New-ScheduledTaskPrincipal `
    -UserId $User `
    -LogonType Interactive `
    -RunLevel Limited
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Principal $Principal `
    -Settings $Settings `
    -Description "Runs candidate-only moderation post generation for next-day manual Streamlit review. Does not approve, merge, or publish content." `
    -Force | Out-Null

Write-Host "Registered scheduled task: $TaskName"
Write-Host "Runs daily at: $At"
Write-Host "Action:"
Write-Host "  powershell.exe $Argument"
Write-Host "This task creates candidates only. It does not approve content or touch Unity."
