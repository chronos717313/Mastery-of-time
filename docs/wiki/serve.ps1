# TMT v2.4 Wiki Server - PowerShell Script
# Double-click or run: .\serve.ps1

$env:PYTHONPATH = "C:\Users\cades\AppData\Roaming\Python\Python311\site-packages"
Set-Location $PSScriptRoot
Write-Host "Starting TMT v2.4 Wiki Server..." -ForegroundColor Green
Write-Host "Open your browser to: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
python -m mkdocs serve --dev-addr 127.0.0.1:8000
