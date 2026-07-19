param(
    [string]$TaskName = "Moderation Ensure LM Studio Models",
    [string]$At = "00:45"
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Loader = Join-Path $Root "ensure_lmstudio_models_loaded.ps1"
if (-not (Test-Path -LiteralPath $Loader)) {
    throw "Missing model-loader script: $Loader"
}

$User = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Loader`"" `
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
    -Description "Ensures LM Studio server and moderation generation models are loaded before the 1am candidate-only nightly generation task." `
    -Force | Out-Null

Write-Host "Registered scheduled task: $TaskName"
Write-Host "Runs daily at: $At"
Write-Host "Action:"
Write-Host "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$Loader`""
Write-Host "This task does not generate posts, approve content, or touch Unity."
