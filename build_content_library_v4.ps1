param(
    [string]$ApprovedDir = ".\output\approved",
    [string]$OutputDir = ".\content-library\v4"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Script = Join-Path $Root "scripts\build_content_library_v4.py"
$Overrides = Join-Path $Root "config\v4_overrides.json"

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $Script --approved-dir $ApprovedDir --output-dir $OutputDir --overrides $Overrides
}
elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $Script --approved-dir $ApprovedDir --output-dir $OutputDir --overrides $Overrides
}
else {
    throw "Python was not found on PATH."
}

exit $LASTEXITCODE
