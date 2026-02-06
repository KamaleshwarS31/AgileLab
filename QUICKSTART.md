# 🚀 Quick Start Guide

This guide will help you get the Weather Forecasting System up and running in minutes!

## Prerequisites Checklist

Before you begin, make sure you have:

- [ ] **Node.js 18+** - [Download here](https://nodejs.org/)
- [ ] **Python 3.9+** - [Download here](https://www.python.org/)
- [ ] **PostgreSQL 14+** - [Download here](https://www.postgresql.org/download/)
- [ ] **Redis 6+** - [Download here](https://redis.io/download) or use Docker
- [ ] **OpenWeather API Key** - [Get free key](https://openweathermap.org/api)

## Option 1: Automated Setup (Recommended)

### Windows

```powershell
# Run the setup script
.\setup.ps1
```

### Linux/Mac

```bash
# Make script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

## Option 2: Manual Setup

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit `backend/.env` and add your credentials:

```env
OPENWEATHER_API_KEY=your_api_key_here
DATABASE_URL=postgresql://postgres:password@localhost:5432/weatherdb
REDIS_URL=redis://localhost:6379/0
CORS_ORIGINS=http://localhost:3000
```

### Step 2: Database Setup

```bash
# Create PostgreSQL database
createdb weatherdb

# Or using psql:
psql -U postgres
CREATE DATABASE weatherdb;
\q
```

### Step 3: Start Services

```bash
# Start Redis (if not already running)
redis-server

# Or using Docker:
docker run -d -p 6379:6379 redis:latest
```

### Step 4: Start Backend

```bash
# From backend directory with venv activated
python -m uvicorn app.main:app --reload
```

Backend will be available at:
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

### Step 5: Frontend Setup

Open a **new terminal**:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 🎉 You're Done!

Open your browser and navigate to `http://localhost:3000` to see your weather app!

## Common Issues & Solutions

### Issue: "Module not found" errors in backend

**Solution**: Make sure you're in the virtual environment:
```bash
# Windows
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate
```

### Issue: Database connection error

**Solution**: 
1. Make sure PostgreSQL is running
2. Verify database exists: `psql -l`
3. Check DATABASE_URL in .env file

### Issue: Redis connection error

**Solution**:
1. Make sure Redis is running: `redis-cli ping` (should return "PONG")
2. Check REDIS_URL in .env file

### Issue: API key not working

**Solution**:
1. Verify your OpenWeather API key is active
2. Free tier keys may take a few minutes to activate
3. Check you've added it correctly in backend/.env

### Issue: CORS errors in browser

**Solution**:
1. Make sure backend is running on port 8000
2. Verify CORS_ORIGINS in backend/.env includes `http://localhost:3000`

## Testing the Application

1. **Allow location access** when prompted (or search for a city)
2. **Search for cities**: Try "London", "Tokyo", "New York"
3. **Add favorites**: Click the star icon on weather cards
4. **Toggle theme**: Click the sun/moon icon in bottom-right
5. **View forecasts**: Scroll down to see 7-day forecast

## Next Steps

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🎨 Customize the design in `frontend/app/globals.css`
- 🔧 Add new features by extending the API
- 🚀 Deploy to production (see deployment guide in README)

## Need Help?

- Check the API documentation at `http://localhost:8000/docs`
- Review the implementation plan in `IMPLEMENTATION_PLAN.md`
- Open an issue in the repository

---

**Happy coding! 🌤️**
