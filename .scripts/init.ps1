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