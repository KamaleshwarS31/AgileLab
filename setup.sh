#!/bin/bash

# Weather Forecasting System - Setup Script for Linux/Mac
# This script helps you set up the development environment

echo "🌤️  Weather Forecasting System - Setup Script"
echo "============================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js installed: $(node --version)"
else
    echo "❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python installed: $(python3 --version)"
else
    echo "❌ Python not found. Please install Python 3.9+"
    exit 1
fi

# Check PostgreSQL
echo "⚠️  Please ensure PostgreSQL is installed and running"

# Check Redis
echo "⚠️  Please ensure Redis is installed and running"
echo "   Or use Docker: docker run -d -p 6379:6379 redis:latest"

echo ""
read -p "Continue with setup? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 0
fi

# Setup Backend
echo ""
echo "🔧 Setting up Backend..."

cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your credentials!"
    echo "   You need to add your OpenWeather API key"
fi

cd ..

# Setup Frontend
echo ""
echo "🔧 Setting up Frontend..."

cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

# Final instructions
echo ""
echo "✅ Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo "1. Get your OpenWeather API key from: https://openweathermap.org/api"
echo "2. Edit backend/.env and add your API key"
echo "3. Create PostgreSQL database: createdb weatherdb"
echo "4. Start Redis server"
echo "5. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python -m uvicorn app.main:app --reload"
echo "6. Start the frontend (in a new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "🌐 Access the application at: http://localhost:3000"
echo "📚 API documentation at: http://localhost:8000/docs"
echo ""
echo "Happy coding! 🚀"
