param(
    [string]$WriterModel = "qwen/qwen3.5-9b",
    [string]$EmbeddingModel = "text-embedding-nomic-embed-text-v1.5",
    [string]$Endpoint = "http://127.0.0.1:1234",
    [int]$TimeoutSeconds = 180
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$ReportDir = Join-Path $Root "output\nightly-reports"
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null

$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$ReportPath = Join-Path $ReportDir "lmstudio-model-loader-$Stamp.md"
$LogLines = New-Object System.Collections.Generic.List[string]

function Write-Log {
    param([string]$Message)
    $Line = "[$((Get-Date).ToString('s'))] $Message"
    $LogLines.Add($Line)
    Write-Host $Line
}

function Save-Report {
    param(
        [string]$Status,
        [bool]$ServerReachable,
        [bool]$WriterAvailable,
        [bool]$EmbeddingAvailable,
        [string]$FailureMessage = ""
    )

    $Lines = @(
        "# LM Studio Model Loader Report",
        "",
        "Timestamp: $((Get-Date).ToString('s'))",
        "Status: $Status",
        "Endpoint: $Endpoint",
        "Writer model: $WriterModel",
        "Embedding model: $EmbeddingModel",
        "Server reachable: $ServerReachable",
        "Writer model loaded/available: $WriterAvailable",
        "Embedding model loaded/available: $EmbeddingAvailable",
        "Failure message: $FailureMessage",
        "",
        "Safety confirmations:",
        "- No posts were generated.",
        "- No candidates were modified.",
        "- No content was approved.",
        "- Nothing was published to Unity.",
        "",
        "Log:",
        $($LogLines | ForEach-Object { "- $_" })
    )
    $Lines | Set-Content -LiteralPath $ReportPath -Encoding UTF8
}

function Test-Endpoint {
    try {
        Invoke-RestMethod `
            -Uri "$Endpoint/v1/models" `
            -Method Get `
            -TimeoutSec 8 `
            -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Get-LoadedModels {
    try {
        $Raw = & lms ps --json 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "lms ps --json failed: $Raw"
        }
        if (-not $Raw) {
            return @()
        }
        return @(($Raw | Out-String | ConvertFrom-Json))
    }
    catch {
        Write-Log "Could not parse loaded model list: $($_.Exception.Message)"
        return @()
    }
}

function Test-ModelLoaded {
    param(
        [object[]]$LoadedModels,
        [string]$ModelId
    )
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

function Load-ModelIfMissing {
    param(
        [string]$ModelId,
        [string]$Kind
    )

    $Loaded = Get-LoadedModels
    if (Test-ModelLoaded -LoadedModels $Loaded -ModelId $ModelId) {
        Write-Log "$Kind model already loaded: $ModelId"
        return
    }

    Write-Log "Loading $Kind model: $ModelId"
    $Output = & lms load $ModelId --identifier $ModelId --yes 2>&1
    $Exit = $LASTEXITCODE
    foreach ($Line in @($Output)) {
        if ($Line) {
            Write-Log "lms load: $Line"
        }
    }
    if ($Exit -ne 0) {
        throw "Failed to load $Kind model '$ModelId' with lms load. If this is the embedding model and the CLI cannot load it in this LM Studio version, load it manually in LM Studio and rerun this script."
    }
}

if ($TimeoutSeconds -le 0) {
    Write-Error "TimeoutSeconds must be greater than zero."
    exit 2
}

$LmsCommand = Get-Command lms -ErrorAction SilentlyContinue
if (-not $LmsCommand) {
    $Message = "The 'lms' CLI was not found. Install LM Studio, enable/install the LM Studio CLI, ensure it is on PATH, then reopen PowerShell and rerun this script."
    Write-Log $Message
    Save-Report -Status "failed_lms_cli_missing" -ServerReachable $false -WriterAvailable $false -EmbeddingAvailable $false -FailureMessage $Message
    Write-Error $Message
    exit 2
}

Write-Log "Using lms CLI: $($LmsCommand.Source)"

$ServerReachable = Test-Endpoint
if (-not $ServerReachable) {
    Write-Log "LM Studio server is not reachable at $Endpoint/v1/models. Starting local server."
    $Port = ([uri]$Endpoint).Port
    if (-not $Port -or $Port -le 0) {
        $Port = 1234
    }
    $ServerOutput = & lms server start --port $Port --bind 127.0.0.1 2>&1
    foreach ($Line in @($ServerOutput)) {
        if ($Line) {
            Write-Log "lms server start: $Line"
        }
    }
}
else {
    Write-Log "LM Studio server already reachable at $Endpoint/v1/models."
}

$Deadline = (Get-Date).AddSeconds($TimeoutSeconds)
while ((Get-Date) -lt $Deadline) {
    if (Test-Endpoint) {
        $ServerReachable = $true
        break
    }
    Start-Sleep -Seconds 3
}

if (-not $ServerReachable) {
    $Message = "LM Studio server did not respond at $Endpoint/v1/models within $TimeoutSeconds seconds."
    Write-Log $Message
    Save-Report -Status "failed_server_unreachable" -ServerReachable $false -WriterAvailable $false -EmbeddingAvailable $false -FailureMessage $Message
    Write-Error $Message
    exit 3
}

try {
    Load-ModelIfMissing -ModelId $WriterModel -Kind "writer"
    Load-ModelIfMissing -ModelId $EmbeddingModel -Kind "embedding"

    $LoadedAfter = Get-LoadedModels
    $WriterAvailable = Test-ModelLoaded -LoadedModels $LoadedAfter -ModelId $WriterModel
    $EmbeddingAvailable = Test-ModelLoaded -LoadedModels $LoadedAfter -ModelId $EmbeddingModel

    if (-not $WriterAvailable -or -not $EmbeddingAvailable) {
        $Message = "Required models were not both visible in 'lms ps --json' after loading."
        Write-Log $Message
        Save-Report -Status "failed_models_missing_after_load" -ServerReachable $true -WriterAvailable $WriterAvailable -EmbeddingAvailable $EmbeddingAvailable -FailureMessage $Message
        Write-Error $Message
        exit 4
    }

    Write-Log "Writer model loaded/available: $WriterModel"
    Write-Log "Embedding model loaded/available: $EmbeddingModel"
    Save-Report -Status "ready" -ServerReachable $true -WriterAvailable $true -EmbeddingAvailable $true
    Write-Host "LM Studio preflight ready. Report: $ReportPath"
    exit 0
}
catch {
    $LoadedAfterFailure = Get-LoadedModels
    $WriterAvailable = Test-ModelLoaded -LoadedModels $LoadedAfterFailure -ModelId $WriterModel
    $EmbeddingAvailable = Test-ModelLoaded -LoadedModels $LoadedAfterFailure -ModelId $EmbeddingModel
    $Message = $_.Exception.Message
    Write-Log $Message
    Save-Report -Status "failed" -ServerReachable $true -WriterAvailable $WriterAvailable -EmbeddingAvailable $EmbeddingAvailable -FailureMessage $Message
    Write-Error $Message
    exit 5
}
