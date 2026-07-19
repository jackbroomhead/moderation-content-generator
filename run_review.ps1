param(
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"

if (Test-Path $VenvPython) {
    $Python = $VenvPython
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $Python = "python"
}
elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $Python = "py"
}
else {
    throw "Python could not be found. Install Python or restore the Content_Generator .venv folder."
}

Write-Host "Using Python: $Python" -ForegroundColor Cyan

if (-not $SkipInstall) {
    # Check for Streamlit without importing it or writing a traceback to stderr.
    & $Python -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('streamlit') else 1)"

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing review-tool dependency..." -ForegroundColor Yellow
        & $Python -m pip install -r ".\requirements-review.txt"

        if ($LASTEXITCODE -ne 0) {
            throw "The Streamlit installation failed. Review the pip error above."
        }
    }
}

Write-Host "Starting local review page..." -ForegroundColor Green
& $Python -m streamlit run ".\review_app.py"

if ($LASTEXITCODE -ne 0) {
    throw "The review app stopped with exit code $LASTEXITCODE."
}
