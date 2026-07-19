param(
    [switch]$SkipInstall,
    [int]$Port = 8501
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

# LAN review launcher only. Do not port-forward this Streamlit app to the internet.
# Work laptops, VPNs, guest Wi-Fi, and router isolation can block local LAN access.
# Windows Firewall may prompt for access the first time Streamlit binds to the LAN.

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

$LocalIps = @()
if (Get-Command Get-NetIPAddress -ErrorAction SilentlyContinue) {
    $LocalIps = Get-NetIPAddress -AddressFamily IPv4 |
        Where-Object {
            $_.IPAddress -notlike "127.*" -and
            $_.IPAddress -notlike "169.254.*" -and
            $_.PrefixOrigin -ne "WellKnown"
        } |
        Sort-Object InterfaceAlias,IPAddress |
        Select-Object -ExpandProperty IPAddress -Unique
}

if (-not $LocalIps -or $LocalIps.Count -eq 0) {
    $LocalIps = ipconfig |
        Select-String -Pattern "IPv4" |
        ForEach-Object {
            if ($_.Line -match "(\d{1,3}(?:\.\d{1,3}){3})") { $Matches[1] }
        } |
        Where-Object { $_ -notlike "127.*" -and $_ -notlike "169.254.*" } |
        Select-Object -Unique
}

Write-Host "" 
Write-Host "Starting Streamlit review dashboard for LAN access..." -ForegroundColor Green
Write-Host "LAN only: do not expose this dashboard publicly or port-forward it." -ForegroundColor Yellow
Write-Host "If another device cannot connect, check Windows Firewall, VPN, guest Wi-Fi, and router client isolation." -ForegroundColor Yellow
Write-Host "" 
Write-Host "Open on this machine:" -ForegroundColor Cyan
Write-Host "  http://localhost:$Port"
Write-Host "" 
Write-Host "Try from your phone or another laptop on the same Wi-Fi/LAN:" -ForegroundColor Cyan

if ($LocalIps -and $LocalIps.Count -gt 0) {
    foreach ($Ip in $LocalIps) {
        Write-Host "  http://$Ip`:$Port"
    }
}
else {
    Write-Host "  No LAN IPv4 address was detected. Run ipconfig and look for your Wi-Fi/Ethernet IPv4 address." -ForegroundColor Yellow
}

Write-Host "" 
& $Python -m streamlit run ".\review_app.py" --server.address 0.0.0.0 --server.port $Port --server.headless true

if ($LASTEXITCODE -ne 0) {
    throw "The review app stopped with exit code $LASTEXITCODE."
}
