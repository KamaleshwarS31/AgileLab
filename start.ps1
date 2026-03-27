# Weather App Startup Script
# Run this script to start both backend and frontend servers

Write-Host "Starting Weather Forecasting System..." -ForegroundColor Cyan
Write-Host ""

$root = $PSScriptRoot

# Start Backend in a new PowerShell window
Write-Host "Starting Backend Server on http://localhost:8000 ..." -ForegroundColor Green
$backendPath = Join-Path $root "backend"
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; .\venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --reload"

# Wait for backend to start
Start-Sleep -Seconds 4

# Start Frontend in a new PowerShell window
Write-Host "Starting Frontend Server on http://localhost:3000 ..." -ForegroundColor Green
$frontendPath = Join-Path $root "frontend"
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev"

Write-Host ""
Write-Host "Both servers are starting!" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Wait 10-15 seconds, then open: http://localhost:3000" -ForegroundColor Yellow
