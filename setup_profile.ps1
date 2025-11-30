# PowerShell script to setup automatic venv activation
$projectPath = Get-Location
$profilePath = $PROFILE

# Create profile directory if it doesn't exist
$profileDir = Split-Path -Parent $profilePath
if (!(Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force
}

# Content to add to profile
$profileContent = @"
# Auto-activate virtual environment for specific project
if ((Get-Location).Path -eq "$projectPath") {
    if (Test-Path ".\.venv\Scripts\Activate.ps1") {
        & ".\.venv\Scripts\Activate.ps1"
        Write-Host "Virtual environment activated for project" -ForegroundColor Green
    }
}
"@

# Add to profile if not already present
if (!(Test-Path $profilePath) -or !(Get-Content $profilePath -ErrorAction SilentlyContinue | Select-String "Auto-activate virtual environment")) {
    Add-Content -Path $profilePath -Value $profileContent
    Write-Host "PowerShell profile updated. Virtual environment will auto-activate when you navigate to this project directory." -ForegroundColor Green
} else {
    Write-Host "Profile already configured for auto-activation." -ForegroundColor Yellow
}

Write-Host "Setup complete! Restart PowerShell or run: . `$PROFILE" -ForegroundColor Cyan
