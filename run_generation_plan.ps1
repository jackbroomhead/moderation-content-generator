param(
    [string]$PlanPath = ".\generation_plan.json"
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Output = Join-Path $Root "output"
$Logs = Join-Path $Output "automation-logs"
$Archive = Join-Path $Output "checkpoint-archive"
$Lock = Join-Path $Output "generation-run.lock"
$Config = Join-Path $Root "config.json"
$Generator = Join-Path $Root "run_generator.ps1"

New-Item -ItemType Directory -Force -Path $Output,$Logs,$Archive | Out-Null

if (Test-Path $Lock) {
    throw "A generation run is already active: $Lock"
}
if (-not (Test-Path $PlanPath)) {
    throw "Missing generation plan: $PlanPath"
}
if (-not (Test-Path $Config)) {
    throw "Missing config.json: $Config"
}
if (-not (Test-Path $Generator)) {
    throw "Missing run_generator.ps1: $Generator"
}

$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$Backup = Join-Path $Logs "generation-$Stamp-config-backup.json"
$Summary = Join-Path $Logs "generation-$Stamp-summary.txt"
$Manifest = Join-Path $Logs "generation-$Stamp-manifest.json"
$RunLog = Join-Path $Logs "generation-$Stamp-run.log"
$Progress = Join-Path $Logs "generation-$Stamp-progress.json"

Copy-Item $Config $Backup -Force
"started=$((Get-Date).ToString('s'))" | Set-Content $Lock -Encoding UTF8

$Plan = Get-Content $PlanPath -Raw | ConvertFrom-Json
$Results = @()
$AnyFailure = $false
$FatalError = $null
$DiversityRetrySuffix = @"
NIGHTLY DIVERSITY RETRY:
- Avoid every theme, setting and policy angle that failed earlier in this profile.
- Avoid hobby/craft/baking/gardening/public-notice templates.
- Do not use "finally finished", pottery, sourdough, candles, vinyl, library notices, community festivals, obvious credential-verification scams, or generic public-safety rumour templates.
- Change scenario type, author voice, tone, text structure, metadata tuple and policy category where the blueprint allows it.
- Prefer sharper conflicts and less familiar premises over safe filler.
- For Day 10 and Day 13, prefer specialist misinformation, metadata-aware ambiguity, Needs Review-acceptable cases and hard escalation boundaries over easy approve filler.
- Do not include raw JSON fragments such as "category": inside visible post text.
"@

function Write-RunLog {
    param([string]$Message)
    $Line = "[$((Get-Date).ToString('s'))] $Message"
    $Line | Tee-Object -FilePath $RunLog -Append
}

function Save-Progress {
    param([string]$State = "running")

    [pscustomobject]@{
        state = $State
        updatedAt = (Get-Date).ToString("s")
        runLog = $RunLog
        summary = $Summary
        manifest = $Manifest
        results = $Results
    } |
        ConvertTo-Json -Depth 10 |
        Set-Content $Progress -Encoding UTF8
}

function Archive-Checkpoints {
    param([string]$Label)

    $CheckpointPath = Join-Path $Output "checkpoints"

    if (Test-Path $CheckpointPath) {
        $Items = @(Get-ChildItem $CheckpointPath -Force -ErrorAction SilentlyContinue)
        if ($Items.Count -gt 0) {
            $SafeLabel = $Label -replace '[^A-Za-z0-9_-]', '-'
            $Destination = Join-Path $Archive "$Stamp-$SafeLabel"
            Move-Item $CheckpointPath $Destination
            Write-RunLog "Archived checkpoints to $Destination"
        }
        else {
            Remove-Item $CheckpointPath -Recurse -Force
        }
    }

    New-Item -ItemType Directory -Force -Path $CheckpointPath | Out-Null
}

function Get-NewestAfter {
    param(
        [string]$Folder,
        [string]$Filter,
        [datetime]$After
    )

    if (-not (Test-Path $Folder)) {
        return $null
    }

    Get-ChildItem $Folder -Filter $Filter -File -ErrorAction SilentlyContinue |
        Where-Object { $_.LastWriteTime -ge $After } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
}

function Count-PostsInCandidate {
    param([string]$Path)
    if (-not $Path -or -not (Test-Path -LiteralPath $Path)) {
        return 0
    }
    try {
        $Payload = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
        if ($Payload.posts) {
            return @($Payload.posts).Count
        }
    }
    catch {
        return 0
    }
    return 0
}

function Set-ConfigProperty {
    param(
        [object]$ConfigObject,
        [string]$Name,
        [object]$Value
    )

    if ($ConfigObject.PSObject.Properties[$Name]) {
        $ConfigObject.$Name = $Value
    }
    else {
        $ConfigObject |
            Add-Member `
                -NotePropertyName $Name `
                -NotePropertyValue $Value `
                -Force
    }
}

function Remove-ConfigProperty {
    param(
        [object]$ConfigObject,
        [string]$Name
    )

    if ($ConfigObject.PSObject.Properties[$Name]) {
        $ConfigObject.PSObject.Properties.Remove($Name)
    }
}

try {
    Write-RunLog "Starting generation run."
    Save-Progress -State "running"

    if (-not (Test-NetConnection 127.0.0.1 -Port 1234 -InformationLevel Quiet)) {
        throw "LM Studio is not running on port 1234."
    }

    $CompletedBatches = 0
    $EnabledProfiles = @($Plan.profiles | Where-Object { $_.enabled -eq $true })

    foreach ($Profile in $EnabledProfiles) {
        for ($Batch = 1; $Batch -le [int]$Profile.batches; $Batch++) {
            if ($CompletedBatches -ge [int]$Plan.max_batches_total) {
                break
            }

            $BlueprintPath = Join-Path (
                Join-Path $Root "reference"
            ) ([string]$Profile.blueprint_file)

            if (-not (Test-Path $BlueprintPath)) {
                $AnyFailure = $true
                $Results += [pscustomobject]@{
                    profile = [string]$Profile.name
                    batch = $Batch
                    success = $false
                    attempts = 0
                    candidate = $null
                    validation = $null
                    failureReport = $null
                    error = "Missing blueprint: $BlueprintPath"
                }
                continue
            }

            $CheckpointPath = Join-Path $Output "checkpoints"
            $CheckpointItems = @()
            if (Test-Path $CheckpointPath) {
                $CheckpointItems = @(
                    Get-ChildItem $CheckpointPath -Force -ErrorAction SilentlyContinue
                )
            }

            $IsFirstAttemptedBatch = ($Results.Count -eq 0)
            $ResumeFirst = (
                $Plan.resume_existing_checkpoints_for_first_profile -eq $true
            )

            if (
                $ResumeFirst -and
                $IsFirstAttemptedBatch -and
                $CheckpointItems.Count -gt 0
            ) {
                Write-RunLog (
                    "Resuming existing checkpoints for profile=" +
                    "$($Profile.name), batch=$Batch."
                )
            }
            else {
                Archive-Checkpoints "$($Profile.name)-batch$Batch-pre"
            }

            $BatchStarted = Get-Date
            $PlanRetryAttempts = if ($Plan.retry_attempts_per_profile) {
                [int]$Plan.retry_attempts_per_profile
            }
            elseif ($Plan.retry_failed_batch_once -eq $true) {
                2
            }
            else {
                1
            }
            $ProfileRetryAttempts = if ($Profile.retry_attempts) {
                [int]$Profile.retry_attempts
            }
            else {
                $PlanRetryAttempts
            }
            $MaxAttempts = [Math]::Max(1, $ProfileRetryAttempts)
            $Succeeded = $false
            $Candidate = $null
            $Validation = $null
            $FailureReport = $null
            $LastExitCode = $null
            $AttemptsUsed = 0
            $GeneratedCount = 0
            $FailureReason = ""

            for ($Attempt = 1; $Attempt -le $MaxAttempts; $Attempt++) {
                $AttemptsUsed = $Attempt
                if ($Attempt -gt 1 -and $FailureReport -and $FailureReport.Name -like "*semantic-failed.txt") {
                    Archive-Checkpoints "$($Profile.name)-batch$Batch-semantic-retry$Attempt"
                    Write-RunLog "Archived semantic-failure checkpoints before retry attempt $Attempt."
                }

                $CurrentConfig = Get-Content $Config -Raw | ConvertFrom-Json
                Set-ConfigProperty `
                    -ConfigObject $CurrentConfig `
                    -Name "blueprint_file" `
                    -Value ([string]$Profile.blueprint_file)
                Set-ConfigProperty `
                    -ConfigObject $CurrentConfig `
                    -Name "target_day" `
                    -Value ([int]$Profile.target_day)
                Set-ConfigProperty `
                    -ConfigObject $CurrentConfig `
                    -Name "count" `
                    -Value ([int]$Profile.count)
                if ($Profile.slot_start_index -ne $null) {
                    Set-ConfigProperty `
                        -ConfigObject $CurrentConfig `
                        -Name "slot_start_index" `
                        -Value ([int]$Profile.slot_start_index)
                }
                else {
                    Remove-ConfigProperty `
                        -ConfigObject $CurrentConfig `
                        -Name "slot_start_index"
                }

                $BaseSuffix = [string]$Profile.writer_prompt_suffix
                if (-not $BaseSuffix) {
                    $BaseSuffix = [string]$Plan.writer_prompt_suffix
                }
                if (-not $BaseSuffix) {
                    $BaseSuffix = [string]$CurrentConfig.writer_prompt_suffix
                }
                if ($Attempt -gt 1) {
                    $RetrySuffix = [string]$Profile.diversity_retry_prompt_suffix
                    if (-not $RetrySuffix) {
                        $RetrySuffix = [string]$Plan.diversity_retry_prompt_suffix
                    }
                    if (-not $RetrySuffix) {
                        $RetrySuffix = $DiversityRetrySuffix
                    }
                    Set-ConfigProperty `
                        -ConfigObject $CurrentConfig `
                        -Name "writer_prompt_suffix" `
                        -Value (($BaseSuffix, $RetrySuffix) -join "`n`n")
                }
                else {
                    Set-ConfigProperty `
                        -ConfigObject $CurrentConfig `
                        -Name "writer_prompt_suffix" `
                        -Value $BaseSuffix
                }
                $CurrentConfig |
                    ConvertTo-Json -Depth 20 |
                    Set-Content $Config -Encoding UTF8

                Write-RunLog (
                    "Profile=$($Profile.name), batch=$Batch, " +
                    "attempt=$Attempt of $MaxAttempts"
                )

                & powershell.exe `
                    -NoProfile `
                    -ExecutionPolicy Bypass `
                    -File $Generator *>&1 |
                    Tee-Object -FilePath $RunLog -Append

                $LastExitCode = $LASTEXITCODE

                $Candidate = Get-NewestAfter `
                    -Folder (Join-Path $Output "candidates") `
                    -Filter "*.json" `
                    -After $BatchStarted

                $Validation = Get-NewestAfter `
                    -Folder (Join-Path $Output "reports") `
                    -Filter "*-validation.txt" `
                    -After $BatchStarted

                $FailureReport = Get-NewestAfter `
                    -Folder (Join-Path $Output "reports") `
                    -Filter "*-failed.txt" `
                    -After $BatchStarted

                $ValidationPassed = $false
                if ($Validation) {
                    $ValidationPassed = (
                        Get-Content $Validation.FullName -Raw
                    ) -match 'VALIDATION PASSED'
                }

                # The generator can return exit code 0 after a semantic rejection.
                # A batch counts as successful only when both output files exist
                # and the validation report explicitly says VALIDATION PASSED.
                if (
                    $LastExitCode -eq 0 -and
                    $Candidate -and
                    $Validation -and
                    $ValidationPassed
                ) {
                    $Succeeded = $true
                    $GeneratedCount = Count-PostsInCandidate $Candidate.FullName
                    break
                }

                if ($Attempt -lt $MaxAttempts) {
                    $FailureReason = if ($FailureReport) {
                        "Latest failure report: $($FailureReport.FullName)"
                    }
                    else {
                        "No validation report was produced."
                    }
                    Write-RunLog (
                        "No valid candidate/validation pair was produced. " +
                        "Retrying with diversity hardening."
                    )
                }
            }

            if ($Succeeded) {
                Archive-Checkpoints "$($Profile.name)-batch$Batch-complete"
                $CompletedBatches++
                Write-RunLog "Profile=$($Profile.name), batch=$Batch completed."
            }
            else {
                $AnyFailure = $true
                Archive-Checkpoints "$($Profile.name)-batch$Batch-failed"
                if (-not $FailureReason) {
                    $FailureReason = if ($FailureReport) {
                        "Latest failure report: $($FailureReport.FullName)"
                    }
                    else {
                        "No validated candidate was produced."
                    }
                }
                Write-RunLog (
                    "Profile=$($Profile.name), batch=$Batch failed after " +
                    "$AttemptsUsed attempt(s)."
                )
            }

            $Results += [pscustomobject]@{
                profile = [string]$Profile.name
                batch = $Batch
                requestedCount = [int]$Profile.count
                targetDay = [int]$Profile.target_day
                success = $Succeeded
                attempts = $AttemptsUsed
                exitCode = $LastExitCode
                generatedCount = $GeneratedCount
                candidate = if ($Candidate) { $Candidate.FullName } else { $null }
                validation = if ($Validation) { $Validation.FullName } else { $null }
                failureReport = if ($FailureReport) {
                    $FailureReport.FullName
                }
                else {
                    $null
                }
                error = if ($Succeeded) {
                    $null
                }
                else {
                    $FailureReason
                }
            }

            Save-Progress -State "running"
        }
    }
}
catch {
    $AnyFailure = $true
    $FatalError = $_.Exception.Message
    Write-RunLog "Fatal error: $FatalError"
}
finally {
    if (
        $Plan.restore_original_config -ne $false -and
        (Test-Path $Backup)
    ) {
        Copy-Item $Backup $Config -Force
        Write-RunLog "Restored original config.json."
    }

    if (
        $Plan.unload_models_on_finish -eq $true -and
        (Get-Command lms -ErrorAction SilentlyContinue)
    ) {
        try {
            lms unload --all *>&1 |
                Tee-Object -FilePath $RunLog -Append
            Write-RunLog "Requested unload of all LM Studio models."
        }
        catch {
            Write-RunLog "Model unload warning: $($_.Exception.Message)"
        }
    }

    $Status = if ($AnyFailure) {
        "completed_with_failures"
    }
    else {
        "completed"
    }

    [pscustomobject]@{
        status = $Status
        finishedAt = (Get-Date).ToString("s")
        fatalError = $FatalError
        results = $Results
    } |
        ConvertTo-Json -Depth 10 |
        Set-Content $Manifest -Encoding UTF8

    $Lines = @(
        "Status: $Status"
        "Manifest: $Manifest"
        "Run log: $RunLog"
        ""
    )

    if ($FatalError) {
        $Lines += "Fatal error: $FatalError"
        $Lines += ""
    }

    foreach ($Result in $Results) {
        $Lines += (
            "Profile: $($Result.profile) | Batch: $($Result.batch) | " +
            "Success: $($Result.success) | Attempts: $($Result.attempts) | " +
            "Requested: $($Result.requestedCount) | Generated: $($Result.generatedCount) | " +
            "Target day: $($Result.targetDay)"
        )
        $Lines += "Candidate: $($Result.candidate)"
        $Lines += "Validation: $($Result.validation)"
        $Lines += "Failure report: $($Result.failureReport)"
        $Lines += "Error: $($Result.error)"
        $Lines += ""
    }

    $Lines | Set-Content $Summary -Encoding UTF8
    Save-Progress -State $Status

    if (Test-Path $Lock) {
        Remove-Item $Lock -Force
    }

    Write-Host "Status: $Status"
    Write-Host "Summary: $Summary"
    Write-Host "Manifest: $Manifest"
    Write-Host "Run log: $RunLog"

    if ($AnyFailure) {
        exit 1
    }
}
