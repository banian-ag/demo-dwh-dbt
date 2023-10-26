# add parameter remove to remove all volumes
param(
    [switch]$remove
)
####################################################################
# Initialize virtual environment and install dependencies
####################################################################
Write-Host "Initializing virtual environment and installing dependencies..." -ForegroundColor Cyan
if (!(Test-Path -Path .venv)) {
    python -m venv .venv
}
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Write-Host "...done!`n" -ForegroundColor Cyan

####################################################################
# Download data files
####################################################################
Write-Host "Downloading data files..." -ForegroundColor Cyan
python .\.scripts\data-download\DownloadNycData.py
Write-Host "...done!`n" -ForegroundColor Cyan

####################################################################
# Create volumes folders
####################################################################
Write-Host "Creating volumes folders..." -ForegroundColor Cyan
if ($remove) {
    Write-Host "Removing volumes..." -ForegroundColor Cyan
    if (Test-Path -Path .\.volumes\citus\data-master) {
        Remove-Item -Path .\.volumes\citus\data-master -Recurse -Force
    }
    if (Test-Path -Path .\.volumes\citus\data-worker) {
        Remove-Item -Path .\.volumes\citus\data-worker -Recurse -Force
    }
}
if (!(Test-Path -Path .\.volumes\citus\data-master)) {
    mkdir .\.volumes\citus\data-master
}
if (!(Test-Path -Path .\.volumes\citus\data-worker)) {
    mkdir .\.volumes\citus\data-worker
}
if (!(Test-Path -Path .\.volumes\citus\init)) {
    mkdir .\.volumes\citus\init
}
Write-Host "...done!`n" -ForegroundColor Cyan

####################################################################
# Create local env file
####################################################################
Write-Host "Creating local env file..." -ForegroundColor Cyan
python .\.scripts\docker-env\BuildLocalEnvFile.py
Write-Host "...done!`n" -ForegroundColor Cyan

####################################################################
# Start docker compose
####################################################################
Write-Host "Starting docker compose..." -ForegroundColor Cyan
docker compose --env-file .env.local up -d
Write-Host "...done!`n" -ForegroundColor Cyan

####################################################################
# Load the raw data
####################################################################
Write-Host "Start data load..." -ForegroundColor Cyan
Start-Sleep -s 20
python .\.scripts\data-load\LoadNycData.py
Write-Host "...done!`n" -ForegroundColor Cyan