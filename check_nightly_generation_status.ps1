$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Output = Join-Path $Root "output"
$Logs = Join-Path $Output "automation-logs"
$CandidateDir = Join-Path $Output "candidates"
$ReportDir = Join-Path $Output "reports"
$NightlyPlanDir = Join-Path $Output "nightly-plans"
$NightlyReportDir = Join-Path $Output "nightly-reports"
$Lock = Join-Path $Output "generation-run.lock"
$Endpoint = "http://127.0.0.1:1234"

function Test-LmStudio {
    try {
        Invoke-RestMethod `
            -Uri "$Endpoint/v1/models" `
            -Method Get `
            -TimeoutSec 5 `
            -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Get-LatestFile {
    param(
        [string]$Folder,
        [string]$Filter
    )
    if (-not (Test-Path -LiteralPath $Folder)) {
        return $null
    }
    Get-ChildItem -LiteralPath $Folder -Filter $Filter -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
}

function Get-ActiveGenerationProcesses {
    try {
        @(
            Get-CimInstance Win32_Process -ErrorAction Stop |
                Where-Object {
                    $_.CommandLine -match "run_generation_plan\.ps1|run_generator\.ps1|generate_posts\.py"
                }
        )
    }
    catch {
        Write-Host "Warning: could not inspect active generation processes: $($_.Exception.Message)"
        @()
    }
}

function Read-Posts {
    param([string]$Path)
    if (-not $Path -or -not (Test-Path -LiteralPath $Path)) {
        return @()
    }
    try {
        $Payload = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
        if ($Payload.posts) {
            return @($Payload.posts)
        }
    }
    catch {
        return @()
    }
    return @()
}

function Count-MatchingLines {
    param(
        [string[]]$Paths,
        [string]$Pattern
    )
    $Count = 0
    foreach ($Path in $Paths) {
        if ($Path -and (Test-Path -LiteralPath $Path)) {
            $Count += @(
                Select-String -LiteralPath $Path -Pattern $Pattern -ErrorAction SilentlyContinue
            ).Count
        }
    }
    return $Count
}

$LockExists = Test-Path -LiteralPath $Lock
$LmReachable = Test-LmStudio
$Active = Get-ActiveGenerationProcesses
$LatestPlan = Get-LatestFile -Folder $NightlyPlanDir -Filter "generation-plan-*.json"
$LatestNightlyReport = Get-LatestFile -Folder $NightlyReportDir -Filter "nightly-report-*.md"
$LatestManifest = Get-LatestFile -Folder $Logs -Filter "generation-*-manifest.json"

$LatestCandidates = @()
$LatestValidations = @()
if ($LatestManifest) {
    try {
        $Manifest = Get-Content -LiteralPath $LatestManifest.FullName -Raw | ConvertFrom-Json
        foreach ($Result in @($Manifest.results)) {
            if ($Result.candidate) {
                $LatestCandidates += [string]$Result.candidate
            }
            if ($Result.validation) {
                $LatestValidations += [string]$Result.validation
            }
            if ($Result.failureReport) {
                $LatestValidations += [string]$Result.failureReport
            }
        }
    }
    catch {
        $LatestCandidates = @()
        $LatestValidations = @()
    }
}

if ($LatestCandidates.Count -eq 0 -and (Test-Path -LiteralPath $CandidateDir)) {
    $LatestCandidates = @(
        Get-ChildItem -LiteralPath $CandidateDir -Filter "*.json" -File -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 8 |
            ForEach-Object { $_.FullName }
    )
}
if ($LatestValidations.Count -eq 0 -and (Test-Path -LiteralPath $ReportDir)) {
    $LatestValidations = @(
        Get-ChildItem -LiteralPath $ReportDir -Filter "*-validation.txt" -File -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 8 |
            ForEach-Object { $_.FullName }
    )
}

$TodayStart = (Get-Date).Date
$TodaysCandidates = @()
if (Test-Path -LiteralPath $CandidateDir) {
    $TodaysCandidates = @(
        Get-ChildItem -LiteralPath $CandidateDir -Filter "*.json" -File -ErrorAction SilentlyContinue |
            Where-Object { $_.LastWriteTime -ge $TodayStart }
    )
}
$TodaysPostCount = 0
foreach ($Candidate in $TodaysCandidates) {
    $TodaysPostCount += @(Read-Posts -Path $Candidate.FullName).Count
}

$BlockingErrors = Count-MatchingLines -Paths $LatestValidations -Pattern "VALIDATION ERRORS|Blocking errors: [1-9]"
$Warnings = Count-MatchingLines -Paths $LatestValidations -Pattern "WARNING|Warning|warnings"
$PolicyWarnings = Count-MatchingLines -Paths $LatestValidations -Pattern "Policy heuristic|policy-quality"
$ValidationPassed = $true
foreach ($Validation in $LatestValidations) {
    if (
        $Validation -like "*-validation.txt" -and
        (Test-Path -LiteralPath $Validation) -and
        -not ((Get-Content -LiteralPath $Validation -Raw) -match "VALIDATION PASSED")
    ) {
        $ValidationPassed = $false
    }
}
if ($LatestValidations.Count -eq 0) {
    $ValidationPassed = $false
}

$ReadyForReview = (
    -not $LockExists -and
    $Active.Count -eq 0 -and
    $LatestCandidates.Count -gt 0 -and
    $ValidationPassed -and
    $BlockingErrors -eq 0
)

Write-Host "Nightly generation status"
Write-Host "========================="
Write-Host "generation-run.lock exists: $LockExists"
if ($LockExists) {
    Write-Host "Lock path: $Lock"
}
Write-Host "Active generation processes: $($Active.Count)"
Write-Host "LM Studio reachable at $Endpoint`: $LmReachable"
Write-Host ""
Write-Host "Latest generation plan: $(if ($LatestPlan) { $LatestPlan.FullName } else { '<none>' })"
Write-Host "Latest generation manifest: $(if ($LatestManifest) { $LatestManifest.FullName } else { '<none>' })"
Write-Host "Latest nightly report: $(if ($LatestNightlyReport) { $LatestNightlyReport.FullName } else { '<none>' })"
Write-Host ""
Write-Host "Latest candidate files:"
if ($LatestCandidates.Count -gt 0) {
    foreach ($Candidate in $LatestCandidates) {
        $Count = @(Read-Posts -Path $Candidate).Count
        Write-Host "  $Candidate ($Count posts)"
    }
}
else {
    Write-Host "  <none>"
}
Write-Host ""
Write-Host "Latest validation reports:"
if ($LatestValidations.Count -gt 0) {
    foreach ($Validation in $LatestValidations) {
        Write-Host "  $Validation"
    }
}
else {
    Write-Host "  <none>"
}
Write-Host ""
Write-Host "Candidate posts generated today: $TodaysPostCount"
Write-Host "Blocking errors: $BlockingErrors"
Write-Host "Warnings: $Warnings"
Write-Host "Policy-quality warnings: $PolicyWarnings"
Write-Host "Candidates ready for Streamlit review: $ReadyForReview"
Write-Host ""
Write-Host "Open local review dashboard:"
Write-Host "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review.ps1"
Write-Host "Open LAN review dashboard:"
Write-Host "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review_lan.ps1"

if ($LockExists -or $Active.Count -gt 0) {
    exit 2
}
if ($BlockingErrors -gt 0) {
    exit 1
}
