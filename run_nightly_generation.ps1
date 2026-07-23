param(
    [int]$TotalPosts = 40,
    [int[]]$Days = @(),
    [string]$DaysCsv = "3,6,10,13",
    [int]$MaxRuntimeMinutes = 360,
    [int]$RetryAttemptsPerProfile = 4,
    [string]$StrategyPath = ".\config\nightly_generation_strategy.json",
    [bool]$UnloadModelsOnFinish = $true,
    [string]$WriterModelToUnload = "",
    [string]$EmbeddingModelToUnload = "",
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

function Resolve-Days {
    param(
        [int[]]$DaysArgument,
        [string]$DaysCsvArgument
    )

    $Resolved = @()
    if ($DaysArgument -and $DaysArgument.Count -gt 0) {
        $Resolved = @($DaysArgument)
    }
    else {
        $Parts = @($DaysCsvArgument -split '[,\s]+' | Where-Object { $_ -and $_.Trim() })
        foreach ($Part in $Parts) {
            $Value = 0
            if (-not [int]::TryParse($Part.Trim(), [ref]$Value)) {
                throw "Invalid day value '$Part' in DaysCsv. Use a comma-separated list such as -DaysCsv `"3,6,10,13`"."
            }
            $Resolved += $Value
        }
    }

    $Unique = @($Resolved | Sort-Object -Unique)
    if (-not $Unique -or $Unique.Count -eq 0) {
        throw "At least one day must be selected. Use -DaysCsv `"3,6,10,13`"."
    }
    if ($Unique.Count -eq 1 -and $Unique[0] -gt 99) {
        throw "Suspicious day value '$($Unique[0])'. This usually means a comma list was collapsed by Task Scheduler. Use -DaysCsv `"3,6,10,13`" instead of -Days."
    }
    foreach ($Day in $Unique) {
        if ($Day -lt 0 -or $Day -gt 99) {
            throw "Invalid day '$Day'. Expected day values between 0 and 99."
        }
    }
    return $Unique
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

function Get-TrimmedFileText {
    param([string]$Path)
    if (-not $Path -or -not (Test-Path -LiteralPath $Path)) {
        return ""
    }

    $Raw = Get-Content -LiteralPath $Path -Raw -ErrorAction SilentlyContinue
    if ($null -eq $Raw) {
        return ""
    }

    return $Raw.Trim()
}

function Get-LmsCommandPath {
    $Preferred = "C:\Users\jackb\.lmstudio\bin\lms.exe"
    if (Test-Path -LiteralPath $Preferred) {
        return $Preferred
    }

    $Command = Get-Command lms -ErrorAction SilentlyContinue
    if ($Command) {
        return $Command.Source
    }

    return ""
}

function Get-LoadedLmStudioModels {
    param([string]$LmsPath)
    if (-not $LmsPath) {
        return @()
    }

    try {
        $PreviousPreference = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        try {
            $Raw = & $LmsPath ps --json 2>&1
            $ExitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $PreviousPreference
        }
        if ($ExitCode -ne 0 -or -not $Raw) {
            return @()
        }
        return @(($Raw | Out-String | ConvertFrom-Json))
    }
    catch {
        return @()
    }
}

function Test-LmStudioModelLoaded {
    param(
        [object[]]$LoadedModels,
        [string]$ModelId
    )
    if (-not $ModelId) {
        return $false
    }

    foreach ($Model in $LoadedModels) {
        $Values = @(
            [string]$Model.modelKey,
            [string]$Model.identifier,
            [string]$Model.indexedModelIdentifier,
            [string]$Model.path,
            [string]$Model.selectedVariant
        )
        foreach ($Value in $Values) {
            if ($Value -eq $ModelId -or $Value -like "*$ModelId*") {
                return $true
            }
        }
    }
    return $false
}

function Invoke-LmStudioModelUnload {
    param(
        [string]$LmsPath,
        [string]$ModelId,
        [string]$Kind
    )

    $Result = [pscustomobject]@{
        Attempted = $false
        Warning = ""
    }
    if (-not $LmsPath) {
        $Result.Warning = "Could not find lms CLI; skipped $Kind model unload."
        return $Result
    }
    if (-not $ModelId) {
        $Result.Warning = "No $Kind model identifier was provided; skipped unload."
        return $Result
    }

    $LoadedBefore = Get-LoadedLmStudioModels -LmsPath $LmsPath
    if (-not (Test-LmStudioModelLoaded -LoadedModels $LoadedBefore -ModelId $ModelId)) {
        $Result.Warning = "$Kind model was already unloaded: $ModelId"
        return $Result
    }

    $Result.Attempted = $true
    try {
        $PreviousPreference = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        try {
            $Output = & $LmsPath unload $ModelId 2>&1
            $ExitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $PreviousPreference
        }
        if ($ExitCode -ne 0) {
            $Result.Warning = "Failed to unload $Kind model '$ModelId': $($Output -join ' ')"
        }
        elseif ($Output) {
            $Result.Warning = "$Kind unload output: $($Output -join ' ')"
        }
    }
    catch {
        $Result.Warning = "Failed to unload $Kind model '$ModelId': $($_.Exception.Message)"
    }

    return $Result
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
        [string]$WrapperStdOutPath = "",
        [string]$WrapperStdErrPath = "",
        [string]$ChildSummaryPath = "",
        [bool]$UnloadRequested = $false,
        [bool]$WriterUnloadAttempted = $false,
        [bool]$EmbeddingUnloadAttempted = $false,
        [bool]$WriterStillLoadedAfterUnload = $false,
        [bool]$EmbeddingStillLoadedAfterUnload = $false,
        [string[]]$UnloadWarnings = @(),
        [string]$FailureMessage = ""
    )

    $Manifest = $null
    if ($ManifestPath -and (Test-Path -LiteralPath $ManifestPath)) {
        $Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    }

    $CandidateFiles = @()
    $ValidationFiles = @()
    $ProfileLines = @()
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
            $ProfileLines += (
                "- {0}: day={1}, requested={2}, generated={3}, success={4}, " +
                "attempts={5}, failure={6}"
            ) -f @(
                [string]$Result.profile,
                [string]$Result.targetDay,
                [string]$Result.requestedCount,
                [string]$Result.generatedCount,
                [string]$Result.success,
                [string]$Result.attempts,
                [string]$Result.error
            )
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
    $GeneratedDays = @(
        $Posts |
            ForEach-Object { [int]($_.day) } |
            Sort-Object -Unique
    )
    $MissingDays = @(
        $RequestedDays |
            Where-Object { $GeneratedDays -notcontains [int]$_ }
    )

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
    $StdOutTail = @()
    $StdErrTail = @()
    $SummaryTail = @()
    if ($WrapperStdOutPath -and (Test-Path -LiteralPath $WrapperStdOutPath)) {
        $StdOutTail = @(Get-Content -LiteralPath $WrapperStdOutPath -Tail 40)
    }
    if ($WrapperStdErrPath -and (Test-Path -LiteralPath $WrapperStdErrPath)) {
        $StdErrTail = @(Get-Content -LiteralPath $WrapperStdErrPath -Tail 40)
    }
    if ($ChildSummaryPath -and (Test-Path -LiteralPath $ChildSummaryPath)) {
        $SummaryTail = @(Get-Content -LiteralPath $ChildSummaryPath -Tail 80)
    }
    $ReadyForReview = (
        $Status -eq "completed" -and
        $ValidationPassed -and
        $BlockingErrors -eq 0 -and
        $CandidateFiles.Count -gt 0 -and
        $MissingDays.Count -eq 0
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
        "Child summary: $ChildSummaryPath",
        "Wrapper stdout: $WrapperStdOutPath",
        "Wrapper stderr: $WrapperStdErrPath",
        "Model endpoint: $Endpoint",
        "LM Studio check: $LmStudioDetail",
        "LM Studio loaded models: $($LmStudioModels -join ', ')",
        "Writer model: $($Config.model)",
        "Embedding model: $($Config.embedding_model)",
        "Requested TotalPosts: $RequestedTotal",
        "Requested Days: $($RequestedDays -join ',')",
        "Generated Days: $($GeneratedDays -join ',')",
        "Missing Expected Days: $($MissingDays -join ',')",
        "Per-profile results:",
        $ProfileLines,
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
        "Unload requested: $UnloadRequested",
        "Writer unload attempted: $WriterUnloadAttempted",
        "Embedding unload attempted: $EmbeddingUnloadAttempted",
        "Writer still loaded after unload: $WriterStillLoadedAfterUnload",
        "Embedding still loaded after unload: $EmbeddingStillLoadedAfterUnload",
        "Unload warnings/errors:",
        $($UnloadWarnings | ForEach-Object { "- $_" }),
        "",
        "Child summary tail:",
        $($SummaryTail | ForEach-Object { "- $_" }),
        "",
        "Wrapper stdout tail:",
        $($StdOutTail | ForEach-Object { "- $_" }),
        "",
        "Wrapper stderr tail:",
        $($StdErrTail | ForEach-Object { "- $_" }),
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
if ($MaxRuntimeMinutes -le 0) {
    throw "MaxRuntimeMinutes must be greater than zero."
}
if ($RetryAttemptsPerProfile -le 0) {
    throw "RetryAttemptsPerProfile must be greater than zero."
}
if (-not (Test-Path -LiteralPath $Runner)) {
    throw "Missing generation plan runner: $Runner"
}
if (-not (Test-Path -LiteralPath $ConfigPath)) {
    throw "Missing config.json: $ConfigPath"
}

$UniqueDays = @(Resolve-Days -DaysArgument $Days -DaysCsvArgument $DaysCsv)

$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
if (-not $Label) {
    $Label = "nightly-$Stamp"
}
$SafeLabel = Get-SafeLabel -Value $Label
$PlanPath = Join-Path $PlanDir "generation-plan-$SafeLabel-$Stamp.json"
$ReportPath = Join-Path $ReportDir "nightly-report-$SafeLabel-$Stamp.md"
$WrapperOut = Join-Path $Logs "nightly-$SafeLabel-$Stamp-stdout.log"
$WrapperErr = Join-Path $Logs "nightly-$SafeLabel-$Stamp-stderr.log"
$UnloadFlagText = if ($UnloadModelsOnFinish) { '$true' } else { '$false' }
$CommandUsed = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_nightly_generation.ps1 -TotalPosts $TotalPosts -DaysCsv `"$($UniqueDays -join ',')`" -MaxRuntimeMinutes $MaxRuntimeMinutes -RetryAttemptsPerProfile $RetryAttemptsPerProfile -UnloadModelsOnFinish $UnloadFlagText -Label `"$Label`""

$Config = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
$Strategy = $null
$ResolvedStrategyPath = if ([System.IO.Path]::IsPathRooted($StrategyPath)) {
    $StrategyPath
}
else {
    Join-Path $Root $StrategyPath
}
if (Test-Path -LiteralPath $ResolvedStrategyPath) {
    $Strategy = Get-Content -LiteralPath $ResolvedStrategyPath -Raw | ConvertFrom-Json
}
if (-not $WriterModelToUnload) {
    $WriterModelToUnload = [string]$Config.model
}
if (-not $EmbeddingModelToUnload) {
    $EmbeddingModelToUnload = [string]$Config.embedding_model
}
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
        -RequestedDays $UniqueDays `
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
        -RequestedDays $UniqueDays `
        -LmStudioDetail $LmStudio.Detail `
        -LmStudioModels $LmStudio.Models `
        -FailureMessage "Existing generation-run.lock or active generation process found." | Out-Null
    Write-Host "A generation run is already active or locked. Refusing to start another run."
    Write-Host "Lock exists: $(Test-Path -LiteralPath $Lock)"
    Write-Host "Active generation processes: $($Active.Count)"
    Write-Host "Nightly report: $ReportPath"
    exit 3
}

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
    $DayStrategy = $null
    if ($Strategy -and $Strategy.day_profiles) {
        $DayProperty = $Strategy.day_profiles.PSObject.Properties[[string]$Day]
        if ($DayProperty) {
            $DayStrategy = $DayProperty.Value
        }
    }
    $FocusParts = @()
    if ($Strategy -and $Strategy.default_focus) {
        $FocusParts += [string]$Strategy.default_focus
    }
    if ($DayStrategy -and $DayStrategy.focus) {
        $FocusParts += [string]$DayStrategy.focus
    }
    $ProfileRetryAttempts = if ($Strategy -and $Strategy.retry_attempts_per_profile) {
        [int]$Strategy.retry_attempts_per_profile
    }
    else {
        $RetryAttemptsPerProfile
    }
    $SlotStartIndex = if ($DayStrategy -and $DayStrategy.slot_start_index -ne $null) {
        [int]$DayStrategy.slot_start_index
    }
    else {
        0
    }
    $Profiles += [pscustomobject]@{
        name = "$SafeLabel-day$Day"
        enabled = $true
        blueprint_file = Get-BlueprintForDay -Day $Day
        target_day = $Day
        count = $Count
        batches = 1
        retry_attempts = $ProfileRetryAttempts
        slot_start_index = $SlotStartIndex
        writer_prompt_suffix = ($FocusParts -join "`n`n")
    }
}

$Plan = [pscustomobject]@{
    max_batches_total = $Profiles.Count
    retry_failed_batch_once = $false
    retry_attempts_per_profile = $RetryAttemptsPerProfile
    restore_original_config = $true
    unload_models_on_finish = $false
    resume_existing_checkpoints_for_first_profile = $false
    diversity_retry_prompt_suffix = if ($Strategy -and $Strategy.diversity_retry_prompt_suffix) {
        [string]$Strategy.diversity_retry_prompt_suffix
    }
    else {
        ""
    }
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

$TimeoutMilliseconds = [int]($MaxRuntimeMinutes * 60 * 1000)
$Exited = $Process.WaitForExit($TimeoutMilliseconds)
$Process.Refresh()
$TimedOut = -not $Exited -and -not $Process.HasExited
if ($TimedOut) {
    $Progress = Get-ChildItem -LiteralPath $Logs -Filter "generation-*-progress.json" -File -ErrorAction SilentlyContinue |
        Where-Object { $_.LastWriteTime -ge $Started } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    $ProgressManifest = ""
    $ProgressRunLog = ""
    $ProgressSummary = ""
    if ($Progress) {
        try {
            $ProgressJson = Get-Content -LiteralPath $Progress.FullName -Raw | ConvertFrom-Json
            $ProgressManifest = [string]$ProgressJson.manifest
            $ProgressRunLog = [string]$ProgressJson.runLog
            $ProgressSummary = [string]$ProgressJson.summary
        }
        catch {
            $ProgressManifest = ""
            $ProgressRunLog = ""
            $ProgressSummary = ""
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
        -WrapperStdOutPath $WrapperOut `
        -WrapperStdErrPath $WrapperErr `
        -ChildSummaryPath $ProgressSummary `
        -UnloadRequested $UnloadModelsOnFinish `
        -UnloadWarnings @("Skipped model unload because generation may still be running after timeout.") `
        -FailureMessage "MaxRuntimeMinutes elapsed. The generation process was not killed; check status before starting another run." | Out-Null
    Write-Host "MaxRuntimeMinutes elapsed. Generation process was not killed."
    Write-Host "Check status with:"
    Write-Host "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\check_nightly_generation_status.ps1"
    Write-Host "Nightly report: $ReportPath"
    exit 124
}

$Process.Refresh()
$ExitCode = $Process.ExitCode
$ManifestFile = Get-ChildItem -LiteralPath $Logs -Filter "generation-*-manifest.json" -File -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -ge $Started -and -not $BeforeManifests.ContainsKey($_.FullName) } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
$ManifestPath = if ($ManifestFile) { $ManifestFile.FullName } else { "" }
$RunLogPath = ""
$ChildSummaryPath = ""
if ($ManifestPath) {
    $CandidateRunLog = $ManifestPath -replace "-manifest\.json$", "-run.log"
    $CandidateSummary = $ManifestPath -replace "-manifest\.json$", "-summary.txt"
    if (Test-Path -LiteralPath $CandidateRunLog) {
        $RunLogPath = $CandidateRunLog
    }
    if (Test-Path -LiteralPath $CandidateSummary) {
        $ChildSummaryPath = $CandidateSummary
    }
}

$Status = if ($ExitCode -eq 0) { "completed" } else { "completed_with_failures" }
$FailureMessage = ""
if ($ExitCode -ne 0) {
    $StdErrText = Get-TrimmedFileText -Path $WrapperErr
    $StdOutText = Get-TrimmedFileText -Path $WrapperOut
    if ($StdErrText) {
        $FailureMessage = $StdErrText
    }
    elseif ($StdOutText) {
        $FailureMessage = $StdOutText
    }
    else {
        $FailureMessage = "Child generation runner exited with code $ExitCode. See child summary/run log paths in this report."
    }
}

# Write a post-child-exit report before cleanup, then overwrite it below with
# final unload details. This leaves the report path populated even if cleanup
# encounters a non-fatal warning.
Write-NightlyReport `
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
    -LmStudioModels $LmStudio.Models `
    -WrapperStdOutPath $WrapperOut `
    -WrapperStdErrPath $WrapperErr `
    -ChildSummaryPath $ChildSummaryPath `
    -UnloadRequested $UnloadModelsOnFinish `
    -UnloadWarnings @("Model unload pending; final report will overwrite this after cleanup.") `
    -FailureMessage $FailureMessage | Out-Null

$WriterUnloadAttempted = $false
$EmbeddingUnloadAttempted = $false
$WriterStillLoadedAfterUnload = $false
$EmbeddingStillLoadedAfterUnload = $false
$UnloadWarnings = @()
if ($UnloadModelsOnFinish) {
    $LmsPath = Get-LmsCommandPath
    if (-not $LmsPath) {
        $UnloadWarnings += "Could not find lms CLI; skipped model unload."
    }
    else {
        $WriterUnload = Invoke-LmStudioModelUnload `
            -LmsPath $LmsPath `
            -ModelId $WriterModelToUnload `
            -Kind "writer"
        $WriterUnloadAttempted = [bool]$WriterUnload.Attempted
        if ($WriterUnload.Warning) {
            $UnloadWarnings += $WriterUnload.Warning
        }

        $EmbeddingUnload = Invoke-LmStudioModelUnload `
            -LmsPath $LmsPath `
            -ModelId $EmbeddingModelToUnload `
            -Kind "embedding"
        $EmbeddingUnloadAttempted = [bool]$EmbeddingUnload.Attempted
        if ($EmbeddingUnload.Warning) {
            $UnloadWarnings += $EmbeddingUnload.Warning
        }

        $LoadedAfterUnload = Get-LoadedLmStudioModels -LmsPath $LmsPath
        $WriterStillLoadedAfterUnload = Test-LmStudioModelLoaded `
            -LoadedModels $LoadedAfterUnload `
            -ModelId $WriterModelToUnload
        $EmbeddingStillLoadedAfterUnload = Test-LmStudioModelLoaded `
            -LoadedModels $LoadedAfterUnload `
            -ModelId $EmbeddingModelToUnload
    }
}

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
    -LmStudioModels $LmStudio.Models `
    -WrapperStdOutPath $WrapperOut `
    -WrapperStdErrPath $WrapperErr `
    -ChildSummaryPath $ChildSummaryPath `
    -UnloadRequested $UnloadModelsOnFinish `
    -WriterUnloadAttempted $WriterUnloadAttempted `
    -EmbeddingUnloadAttempted $EmbeddingUnloadAttempted `
    -WriterStillLoadedAfterUnload $WriterStillLoadedAfterUnload `
    -EmbeddingStillLoadedAfterUnload $EmbeddingStillLoadedAfterUnload `
    -UnloadWarnings $UnloadWarnings `
    -FailureMessage $FailureMessage

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

