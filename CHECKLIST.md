# ✅ Getting Started Checklist

Use this checklist to get your Weather Forecasting System up and running!

## 📋 Pre-Setup Checklist

### Required Software
- [ ] **Node.js 18+** installed
  - Check: `node --version`
  - Download: https://nodejs.org/

- [ ] **Python 3.9+** installed
  - Check: `python --version`
  - Download: https://www.python.org/

- [ ] **PostgreSQL 14+** installed and running
  - Check: `psql --version`
  - Download: https://www.postgresql.org/download/

- [ ] **Redis 6+** installed and running
  - Check: `redis-cli ping` (should return "PONG")
  - Windows: https://github.com/microsoftarchive/redis/releases
  - Or Docker: `docker run -d -p 6379:6379 redis:latest`

### API Keys
- [ ] **OpenWeather API Key** obtained
  - Sign up: https://openweathermap.org/api
  - Free tier is sufficient
  - Note: May take a few minutes to activate

## 🔧 Setup Checklist

### Option A: Automated Setup (Recommended)

- [ ] Run setup script
  ```powershell
  # Windows
  .\setup.ps1
  
  # Linux/Mac
  chmod +x setup.sh
  ./setup.sh
  ```

- [ ] Edit `backend/.env` with your OpenWeather API key

- [ ] Create PostgreSQL database
  ```bash
  createdb weatherdb
  ```

### Option B: Manual Setup

#### Backend Setup
- [ ] Navigate to backend directory
  ```bash
  cd backend
  ```

- [ ] Create Python virtual environment
  ```bash
  python -m venv venv
  ```

- [ ] Activate virtual environment
  ```powershell
  # Windows
  .\venv\Scripts\Activate.ps1
  
  # Linux/Mac
  source venv/bin/activate
  ```

- [ ] Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Copy environment template
  ```bash
  cp .env.example .env
  ```

- [ ] Edit `.env` file with your credentials
  - [ ] Add OpenWeather API key
  - [ ] Verify DATABASE_URL
  - [ ] Verify REDIS_URL
  - [ ] Set CORS_ORIGINS

#### Database Setup
- [ ] Create PostgreSQL database
  ```bash
  createdb weatherdb
  # Or using psql:
  psql -U postgres
  CREATE DATABASE weatherdb;
  \q
  ```

- [ ] Verify database connection
  ```bash
  psql -U postgres -d weatherdb -c "SELECT 1;"
  ```

#### Frontend Setup
- [ ] Navigate to frontend directory
  ```bash
  cd frontend
  ```

- [ ] Install Node.js dependencies
  ```bash
  npm install
  ```

- [ ] Verify `.env.local` exists and contains:
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```

## 🚀 Running the Application

### Start Services

- [ ] **Start PostgreSQL** (if not already running)
  ```bash
  # Usually runs as a service
  # Check status: pg_ctl status
  ```

- [ ] **Start Redis** (if not already running)
  ```bash
  redis-server
  # Or with Docker:
  docker run -d -p 6379:6379 redis:latest
  ```

### Start Backend

- [ ] Open terminal in `backend` directory

- [ ] Activate virtual environment
  ```powershell
  # Windows
  .\venv\Scripts\Activate.ps1
  
  # Linux/Mac
  source venv/bin/activate
  ```

- [ ] Start FastAPI server
  ```bash
  python -m uvicorn app.main:app --reload
  ```

- [ ] Verify backend is running
  - [ ] Open http://localhost:8000
  - [ ] Should see: `{"message": "Weather Forecasting API", ...}`
  - [ ] Open http://localhost:8000/docs
  - [ ] Should see Swagger documentation

### Start Frontend

- [ ] Open **new terminal** in `frontend` directory

- [ ] Start Next.js development server
  ```bash
  npm run dev
  ```

- [ ] Verify frontend is running
  - [ ] Open http://localhost:3000
  - [ ] Should see the Weather Forecasting app

## ✨ Testing the Application

### Basic Functionality Tests

- [ ] **Location Detection**
  - [ ] Allow browser location access when prompted
  - [ ] Weather should load for your location

- [ ] **Location Search**
  - [ ] Type "London" in search box
  - [ ] Should see autocomplete suggestions
  - [ ] Click a suggestion
  - [ ] Weather should update

- [ ] **Favorites**
  - [ ] Click the star (⭐) icon on weather card
  - [ ] Should turn into filled star
  - [ ] Scroll down to see "Favorite Locations" section
  - [ ] Your location should appear there

- [ ] **Theme Toggle**
  - [ ] Click sun/moon icon in bottom-right
  - [ ] Theme should switch
  - [ ] Refresh page - theme should persist

- [ ] **7-Day Forecast**
  - [ ] Scroll down
  - [ ] Should see 7 forecast cards
  - [ ] Each showing day, icon, temps, precipitation

### API Tests

- [ ] **Test API directly**
  - [ ] Open http://localhost:8000/docs
  - [ ] Try "GET /api/weather/current" endpoint
  - [ ] Use lat=40.7128, lon=-74.0060 (New York)
  - [ ] Should return weather data

- [ ] **Test caching**
  - [ ] Make same API request twice
  - [ ] Second request should be faster (cached)

### Database Tests

- [ ] **Check database**
  ```bash
  psql -U postgres -d weatherdb
  \dt  # List tables
  SELECT * FROM locations LIMIT 5;
  SELECT * FROM weather_history LIMIT 5;
  SELECT * FROM user_favorites;
  \q
  ```

## 🐛 Troubleshooting Checklist

### Backend Issues

- [ ] **"Module not found" error**
  - [ ] Verify virtual environment is activated
  - [ ] Run `pip install -r requirements.txt` again

- [ ] **Database connection error**
  - [ ] Check PostgreSQL is running
  - [ ] Verify DATABASE_URL in .env
  - [ ] Test connection: `psql -U postgres -d weatherdb`

- [ ] **Redis connection error**
  - [ ] Check Redis is running: `redis-cli ping`
  - [ ] Verify REDIS_URL in .env

- [ ] **OpenWeather API error**
  - [ ] Verify API key is correct
  - [ ] Check key is activated (may take a few minutes)
  - [ ] Ensure no extra spaces in .env file

### Frontend Issues

- [ ] **"Cannot connect to backend" error**
  - [ ] Verify backend is running on port 8000
  - [ ] Check NEXT_PUBLIC_API_URL in .env.local
  - [ ] Check CORS_ORIGINS in backend/.env

- [ ] **Blank page**
  - [ ] Check browser console for errors (F12)
  - [ ] Verify npm install completed successfully
  - [ ] Try `npm run dev` again

- [ ] **Styles not loading**
  - [ ] Clear browser cache
  - [ ] Restart development server
  - [ ] Check globals.css is imported in layout.tsx

### General Issues

- [ ] **Port already in use**
  - [ ] Backend (8000): Kill process or use different port
  - [ ] Frontend (3000): Kill process or use different port

- [ ] **Slow performance**
  - [ ] Check Redis is running (caching)
  - [ ] Verify database indexes are created
  - [ ] Check network connection

## 📚 Next Steps After Setup

- [ ] Read through the code to understand structure
- [ ] Explore API documentation at /docs
- [ ] Try adding a new feature
- [ ] Customize the design in globals.css
- [ ] Add more locations to favorites
- [ ] Check historical weather data in database

## 🎯 Production Deployment Checklist

### Frontend (Vercel)
- [ ] Push code to GitHub
- [ ] Create Vercel account
- [ ] Import project
- [ ] Set environment variables
- [ ] Deploy

### Backend (Render/AWS)
- [ ] Set up managed PostgreSQL
- [ ] Set up managed Redis
- [ ] Deploy backend
- [ ] Set environment variables
- [ ] Update frontend API URL

## ✅ Completion Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Can search for locations
- [ ] Can view current weather
- [ ] Can view 7-day forecast
- [ ] Can add/remove favorites
- [ ] Can toggle theme
- [ ] Database storing data
- [ ] Redis caching working

## 🎉 Success!

If all items are checked, congratulations! Your Weather Forecasting System is fully operational!

### What to do next:
1. ⭐ Star the repository (if applicable)
2. 📸 Take screenshots of your app
3. 🚀 Deploy to production
4. 🎨 Customize the design
5. ✨ Add new features
6. 📝 Share your experience

---

**Need help?** Check:
- README.md for detailed documentation
- QUICKSTART.md for setup guide
- ARCHITECTURE.md for system design
- http://localhost:8000/docs for API reference

**Happy coding! 🌤️**
