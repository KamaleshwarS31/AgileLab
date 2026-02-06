# Weather Forecasting System - Setup Script
# This script helps you set up the development environment

Write-Host "🌤️  Weather Forecasting System - Setup Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check Python
try {
    $pythonVersion = python --version
    Write-Host "✅ Python installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.9+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check PostgreSQL
Write-Host "⚠️  Please ensure PostgreSQL is installed and running" -ForegroundColor Yellow
Write-Host "   Download from: https://www.postgresql.org/download/" -ForegroundColor Gray

# Check Redis
Write-Host "⚠️  Please ensure Redis is installed and running" -ForegroundColor Yellow
Write-Host "   Windows: https://github.com/microsoftarchive/redis/releases" -ForegroundColor Gray
Write-Host "   Or use Docker: docker run -d -p 6379:6379 redis:latest" -ForegroundColor Gray

Write-Host ""
$continue = Read-Host "Continue with setup? (y/n)"
if ($continue -ne "y") {
    Write-Host "Setup cancelled." -ForegroundColor Yellow
    exit 0
}

# Setup Backend
Write-Host ""
Write-Host "🔧 Setting up Backend..." -ForegroundColor Cyan

Set-Location backend

# Create virtual environment
Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Please edit backend/.env with your credentials!" -ForegroundColor Yellow
    Write-Host "   You need to add your OpenWeather API key" -ForegroundColor Gray
}

Set-Location ..

# Setup Frontend
Write-Host ""
Write-Host "🔧 Setting up Frontend..." -ForegroundColor Cyan

Set-Location frontend

# Install dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

Set-Location ..

# Final instructions
Write-Host ""
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Get your OpenWeather API key from: https://openweathermap.org/api" -ForegroundColor White
Write-Host "2. Edit backend/.env and add your API key" -ForegroundColor White
Write-Host "3. Create PostgreSQL database: createdb weatherdb" -ForegroundColor White
Write-Host "4. Start Redis server" -ForegroundColor White
Write-Host "5. Start the backend:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   python -m uvicorn app.main:app --reload" -ForegroundColor Gray
Write-Host "6. Start the frontend (in a new terminal):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 Access the application at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "📚 API documentation at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green
