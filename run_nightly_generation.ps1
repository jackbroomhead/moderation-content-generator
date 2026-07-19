param(
    [int]$TotalPosts = 40,
    [int[]]$Days = @(3, 6, 10, 13),
    [int]$MaxRuntimeMinutes = 360,
    [Alias("RunName")]
    [string]$Label = ""
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Output = Join-Path $Root "output"
$Logs = Join-Path $Output "automation-logs"
$PlanDir = Join-Path $Output "nightly-plans"
$ReportDir = Join-Path $Output "nightly-reports"
$Lock = Join-Path $Output "generation-run.lock"
$ConfigPath = Join-Path $Root "config.json"
$Runner = Join-Path $Root "run_generation_plan.ps1"
$Endpoint = "http://127.0.0.1:1234"

New-Item -ItemType Directory -Force -Path $Output,$Logs,$PlanDir,$ReportDir | Out-Null

function Get-SafeLabel {
    param([string]$Value)
    $Clean = $Value -replace '[^A-Za-z0-9_-]', '-'
    $Clean = $Clean.Trim("-")
    if ($Clean) { return $Clean }
    return "nightly"
}

function Test-LmStudio {
    param([string]$BaseUrl)
    try {
        $Response = Invoke-RestMethod `
            -Uri "$BaseUrl/v1/models" `
            -Method Get `
            -TimeoutSec 8 `
            -ErrorAction Stop
        return [pscustomobject]@{
            Reachable = $true
            Detail = "LM Studio responded at $BaseUrl/v1/models."
            Models = @($Response.data | ForEach-Object { $_.id })
        }
    }
    catch {
        return [pscustomobject]@{
            Reachable = $false
            Detail = $_.Exception.Message
            Models = @()
        }
    }
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

function Get-BlueprintForDay {
    param([int]$Day)
    if ($Day -le 1) {
        return "12 - Day 1 Generation Blueprint.json"
    }
    if ($Day -le 5) {
        return "17 - Day 3-5 Escalation Production Blueprint.json"
    }
    if ($Day -le 9) {
        return "20 - Day 6-9 Metadata Blueprint.json"
    }
    if ($Day -le 12) {
        return "21 - Day 10-12 Specialist Misinformation Blueprint.json"
    }
    return "22 - Day 13 Plus Hard Cases Blueprint.json"
}

function Read-Posts {
    param([string]$Path)
    if (-not $Path -or -not (Test-Path -LiteralPath $Path)) {
        return @()
    }
    $Payload = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    if ($Payload.posts) {
        return @($Payload.posts)
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

function Write-NightlyReport {
    param(
        [string]$ReportPath,
        [string]$Status,
        [string]$CommandUsed,
        [string]$PlanPath,
        [string]$ManifestPath,
        [string]$RunLogPath,
        [object]$Config,
        [int]$RequestedTotal,
        [int[]]$RequestedDays,
        [string]$LmStudioDetail,
        [string[]]$LmStudioModels,
        [string]$FailureMessage = ""
    )

    $Manifest = $null
    if ($ManifestPath -and (Test-Path -LiteralPath $ManifestPath)) {
        $Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    }

    $CandidateFiles = @()
    $ValidationFiles = @()
    if ($Manifest) {
        foreach ($Result in @($Manifest.results)) {
            if ($Result.candidate) {
                $CandidateFiles += [string]$Result.candidate
            }
            if ($Result.validation) {
                $ValidationFiles += [string]$Result.validation
            }
            if ($Result.failureReport) {
                $ValidationFiles += [string]$Result.failureReport
            }
        }
    }

    $Posts = @()
    foreach ($Candidate in $CandidateFiles) {
        $Posts += Read-Posts -Path $Candidate
    }

    $Ids = @($Posts | ForEach-Object { $_.id })
    $DayDistribution = @{}
    $ActionDistribution = @{}
    foreach ($Post in $Posts) {
        $Day = [string]$Post.day
        $Action = [string]$Post.correctAction
        if (-not $DayDistribution.ContainsKey($Day)) {
            $DayDistribution[$Day] = 0
        }
        if (-not $ActionDistribution.ContainsKey($Action)) {
            $ActionDistribution[$Action] = 0
        }
        $DayDistribution[$Day]++
        $ActionDistribution[$Action]++
    }

    $ValidationPassed = $true
    foreach ($Validation in $ValidationFiles) {
        if (
            $Validation -like "*-validation.txt" -and
            (Test-Path -LiteralPath $Validation) -and
            -not ((Get-Content -LiteralPath $Validation -Raw) -match "VALIDATION PASSED")
        ) {
            $ValidationPassed = $false
        }
    }
    if (-not $ValidationFiles -or $ValidationFiles.Count -eq 0) {
        $ValidationPassed = $false
    }

    $BlockingErrors = Count-MatchingLines -Paths $ValidationFiles -Pattern "VALIDATION ERRORS|Blocking errors: [1-9]"
    $Warnings = Count-MatchingLines -Paths $ValidationFiles -Pattern "WARNING|Warning|warnings"
    $PolicyWarnings = Count-MatchingLines -Paths $ValidationFiles -Pattern "Policy heuristic|policy-quality"
    $DuplicateNotes = Count-MatchingLines -Paths $ValidationFiles -Pattern "duplicate|similar|SEMANTIC DUPLICATE"
    $ReadyForReview = (
        $Status -eq "completed" -and
        $ValidationPassed -and
        $BlockingErrors -eq 0 -and
        $CandidateFiles.Count -gt 0
    )

    $Lines = @(
        "# Nightly Candidate Generation Report",
        "",
        "Timestamp: $((Get-Date).ToString('s'))",
        "Status: $Status",
        "Command used: $CommandUsed",
        "Plan: $PlanPath",
        "Manifest: $ManifestPath",
        "Run log: $RunLogPath",
        "Model endpoint: $Endpoint",
        "LM Studio check: $LmStudioDetail",
        "LM Studio loaded models: $($LmStudioModels -join ', ')",
        "Writer model: $($Config.model)",
        "Embedding model: $($Config.embedding_model)",
        "Requested TotalPosts: $RequestedTotal",
        "Requested Days: $($RequestedDays -join ',')",
        "Generated candidate files:",
        $($CandidateFiles | ForEach-Object { "- $_" }),
        "Generated candidate count: $($Posts.Count)",
        "Generated IDs: $($Ids -join ', ')",
        "Day distribution: $((@($DayDistribution.GetEnumerator()) | Sort-Object Name | ForEach-Object { "$($_.Name)=$($_.Value)" }) -join ', ')",
        "Action distribution: $((@($ActionDistribution.GetEnumerator()) | Sort-Object Name | ForEach-Object { "$($_.Name)=$($_.Value)" }) -join ', ')",
        "Validation passed: $ValidationPassed",
        "Blocking errors: $BlockingErrors",
        "Warnings: $Warnings",
        "Policy-quality warnings: $PolicyWarnings",
        "Duplicate/near-duplicate notes: $DuplicateNotes",
        "Ready for Streamlit review: $ReadyForReview",
        "Failure message: $FailureMessage",
        "Confirmation: no candidates were approved automatically.",
        "Confirmation: nothing was published to Unity.",
        "Confirmation: Unity StreamingAssets and Assets/Resources/posts.json were not touched by this script.",
        "",
        "Open local review dashboard:",
        "powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review.ps1",
        "",
        "Open LAN review dashboard:",
        "powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review_lan.ps1"
    )

    $Lines | Set-Content -LiteralPath $ReportPath -Encoding UTF8

    return [pscustomobject]@{
        ReadyForReview = $ReadyForReview
        BlockingErrors = $BlockingErrors
        Warnings = $Warnings
        PolicyWarnings = $PolicyWarnings
        CandidateCount = $Posts.Count
        CandidateFiles = $CandidateFiles
    }
}

if ($TotalPosts -le 0) {
    throw "TotalPosts must be greater than zero."
}
if (-not $Days -or $Days.Count -eq 0) {
    throw "At least one day must be selected."
}
if ($MaxRuntimeMinutes -le 0) {
    throw "MaxRuntimeMinutes must be greater than zero."
}
if (-not (Test-Path -LiteralPath $Runner)) {
    throw "Missing generation plan runner: $Runner"
}
if (-not (Test-Path -LiteralPath $ConfigPath)) {
    throw "Missing config.json: $ConfigPath"
}

$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
if (-not $Label) {
    $Label = "nightly-$Stamp"
}
$SafeLabel = Get-SafeLabel -Value $Label
$PlanPath = Join-Path $PlanDir "generation-plan-$SafeLabel-$Stamp.json"
$ReportPath = Join-Path $ReportDir "nightly-report-$SafeLabel-$Stamp.md"
$WrapperOut = Join-Path $Logs "nightly-$SafeLabel-$Stamp-stdout.log"
$WrapperErr = Join-Path $Logs "nightly-$SafeLabel-$Stamp-stderr.log"
$CommandUsed = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_nightly_generation.ps1 -TotalPosts $TotalPosts -Days $($Days -join ',') -MaxRuntimeMinutes $MaxRuntimeMinutes -Label `"$Label`""

$Config = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
$LmStudio = Test-LmStudio -BaseUrl $Endpoint
if (-not $LmStudio.Reachable) {
    Write-NightlyReport `
        -ReportPath $ReportPath `
        -Status "failed_lm_studio_unavailable" `
        -CommandUsed $CommandUsed `
        -PlanPath $PlanPath `
        -ManifestPath "" `
        -RunLogPath "" `
        -Config $Config `
        -RequestedTotal $TotalPosts `
        -RequestedDays $Days `
        -LmStudioDetail $LmStudio.Detail `
        -LmStudioModels @() `
        -FailureMessage "LM Studio is unavailable at $Endpoint. Start LM Studio, load the writer and embedding models, and try again." | Out-Null
    Write-Error "LM Studio is unavailable at $Endpoint. Details: $($LmStudio.Detail)"
    exit 2
}

$Active = Get-ActiveGenerationProcesses
if ((Test-Path -LiteralPath $Lock) -or $Active.Count -gt 0) {
    Write-NightlyReport `
        -ReportPath $ReportPath `
        -Status "blocked_existing_generation_active" `
        -CommandUsed $CommandUsed `
        -PlanPath $PlanPath `
        -ManifestPath "" `
        -RunLogPath "" `
        -Config $Config `
        -RequestedTotal $TotalPosts `
        -RequestedDays $Days `
        -LmStudioDetail $LmStudio.Detail `
        -LmStudioModels $LmStudio.Models `
        -FailureMessage "Existing generation-run.lock or active generation process found." | Out-Null
    Write-Host "A generation run is already active or locked. Refusing to start another run."
    Write-Host "Lock exists: $(Test-Path -LiteralPath $Lock)"
    Write-Host "Active generation processes: $($Active.Count)"
    Write-Host "Nightly report: $ReportPath"
    exit 3
}

$UniqueDays = @($Days | Sort-Object -Unique)
$BaseCount = [math]::Floor($TotalPosts / $UniqueDays.Count)
$Remainder = $TotalPosts % $UniqueDays.Count
$Profiles = @()
for ($Index = 0; $Index -lt $UniqueDays.Count; $Index++) {
    $Day = [int]$UniqueDays[$Index]
    $Count = [int]$BaseCount
    if ($Index -lt $Remainder) {
        $Count++
    }
    if ($Count -le 0) {
        continue
    }
    $Profiles += [pscustomobject]@{
        name = "$SafeLabel-day$Day"
        enabled = $true
        blueprint_file = Get-BlueprintForDay -Day $Day
        target_day = $Day
        count = $Count
        batches = 1
    }
}

$Plan = [pscustomobject]@{
    max_batches_total = $Profiles.Count
    retry_failed_batch_once = $true
    restore_original_config = $true
    unload_models_on_finish = $false
    resume_existing_checkpoints_for_first_profile = $false
    run_label = $Label
    run_kind = "nightly-candidate-generation"
    requested_total_posts = $TotalPosts
    requested_days = $UniqueDays
    profiles = $Profiles
}
$Plan | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $PlanPath -Encoding UTF8

Write-Host "Created nightly generation plan: $PlanPath"
Write-Host "LM Studio reachable: $($LmStudio.Detail)"
Write-Host "Starting candidate-only generation. No approval, merge, or Unity publish step will run."

$Started = Get-Date
$BeforeManifests = @{}
Get-ChildItem -LiteralPath $Logs -Filter "generation-*-manifest.json" -File -ErrorAction SilentlyContinue |
    ForEach-Object { $BeforeManifests[$_.FullName] = $true }

$Arguments = @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-File", "`"$Runner`"",
    "-PlanPath", "`"$PlanPath`""
)

$Process = Start-Process `
    -FilePath "powershell.exe" `
    -ArgumentList $Arguments `
    -WorkingDirectory $Root `
    -RedirectStandardOutput $WrapperOut `
    -RedirectStandardError $WrapperErr `
    -WindowStyle Hidden `
    -PassThru

$TimedOut = -not (Wait-Process -Id $Process.Id -Timeout ($MaxRuntimeMinutes * 60) -ErrorAction SilentlyContinue)
if ($TimedOut) {
    $Progress = Get-ChildItem -LiteralPath $Logs -Filter "generation-*-progress.json" -File -ErrorAction SilentlyContinue |
        Where-Object { $_.LastWriteTime -ge $Started } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    $ProgressManifest = ""
    $ProgressRunLog = ""
    if ($Progress) {
        try {
            $ProgressJson = Get-Content -LiteralPath $Progress.FullName -Raw | ConvertFrom-Json
            $ProgressManifest = [string]$ProgressJson.manifest
            $ProgressRunLog = [string]$ProgressJson.runLog
        }
        catch {
            $ProgressManifest = ""
            $ProgressRunLog = ""
        }
    }

    Write-NightlyReport `
        -ReportPath $ReportPath `
        -Status "timeout_still_running" `
        -CommandUsed $CommandUsed `
        -PlanPath $PlanPath `
        -ManifestPath $ProgressManifest `
        -RunLogPath $ProgressRunLog `
        -Config $Config `
        -RequestedTotal $TotalPosts `
        -RequestedDays $UniqueDays `
        -LmStudioDetail $LmStudio.Detail `
        -LmStudioModels $LmStudio.Models `
        -FailureMessage "MaxRuntimeMinutes elapsed. The generation process was not killed; check status before starting another run." | Out-Null
    Write-Host "MaxRuntimeMinutes elapsed. Generation process was not killed."
    Write-Host "Check status with:"
    Write-Host "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\check_nightly_generation_status.ps1"
    Write-Host "Nightly report: $ReportPath"
    exit 124
}

$ExitCode = $Process.ExitCode
$ManifestFile = Get-ChildItem -LiteralPath $Logs -Filter "generation-*-manifest.json" -File -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -ge $Started -and -not $BeforeManifests.ContainsKey($_.FullName) } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
$ManifestPath = if ($ManifestFile) { $ManifestFile.FullName } else { "" }
$RunLogPath = ""
if ($ManifestPath) {
    $CandidateRunLog = $ManifestPath -replace "-manifest\.json$", "-run.log"
    if (Test-Path -LiteralPath $CandidateRunLog) {
        $RunLogPath = $CandidateRunLog
    }
}

$Status = if ($ExitCode -eq 0) { "completed" } else { "completed_with_failures" }
$ReportResult = Write-NightlyReport `
    -ReportPath $ReportPath `
    -Status $Status `
    -CommandUsed $CommandUsed `
    -PlanPath $PlanPath `
    -ManifestPath $ManifestPath `
    -RunLogPath $RunLogPath `
    -Config $Config `
    -RequestedTotal $TotalPosts `
    -RequestedDays $UniqueDays `
    -LmStudioDetail $LmStudio.Detail `
    -LmStudioModels $LmStudio.Models

Write-Host "Nightly generation finished with status: $Status"
Write-Host "Generated candidate posts: $($ReportResult.CandidateCount)"
Write-Host "Nightly report: $ReportPath"
Write-Host "Open local review dashboard:"
Write-Host "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review.ps1"
Write-Host "Open LAN review dashboard:"
Write-Host "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review_lan.ps1"

if ($ExitCode -ne 0 -or $ReportResult.BlockingErrors -gt 0 -or -not $ReportResult.ReadyForReview) {
    exit 1
}

