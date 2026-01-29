# 🌤️ Weather Forecasting System

A fully functional, feature-packed weather forecasting application with a modern tech stack, beautiful UI, and comprehensive features.

![Weather Forecast](https://img.shields.io/badge/Status-Production%20Ready-success)
![Next.js](https://img.shields.io/badge/Next.js-14+-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue)

## 🚀 Features

### Core Features
- ✅ **Real-time Weather Data** - Current weather conditions with detailed metrics
- ✅ **7-Day Forecast** - Daily weather predictions with temperature ranges
- ✅ **Hourly Forecast** - 48-hour detailed hourly predictions
- ✅ **Location Search** - Search any city worldwide with autocomplete
- ✅ **Geolocation Support** - Automatic detection of user's location
- ✅ **Favorite Locations** - Save and manage multiple locations
- ✅ **Historical Data** - View past weather trends
- ✅ **Responsive Design** - Works seamlessly on all devices

### Premium Features
- 🎨 **Beautiful UI** - Modern, premium design with glassmorphism effects
- 🌓 **Dark/Light Theme** - Toggle between themes with smooth transitions
- 📊 **Interactive Charts** - Visual weather data representation (ready for integration)
- ⚡ **Fast Performance** - Redis caching for optimal speed
- 🔄 **Real-time Updates** - Automatic data refresh
- 💾 **Data Persistence** - PostgreSQL database for historical tracking
- 🎭 **Smooth Animations** - Micro-interactions and transitions

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: CSS Modules with modern CSS features
- **Fonts**: Google Fonts (Inter, Outfit)
- **Deployment**: Vercel-ready

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Cache**: Redis
- **External API**: OpenWeather API
- **Deployment**: AWS/Render-ready

## 📋 Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.9+
- **PostgreSQL** 14+
- **Redis** 6+
- **OpenWeather API Key** (free tier available at [openweathermap.org](https://openweathermap.org/api))

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AgileLab
```

### 2. Backend Setup

#### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
OPENWEATHER_API_KEY=your_openweather_api_key_here
DATABASE_URL=postgresql://postgres:password@localhost:5432/weatherdb
REDIS_URL=redis://localhost:6379/0
CORS_ORIGINS=http://localhost:3000
SECRET_KEY=your-secret-key-here
CACHE_EXPIRATION=300
```

#### Setup Database

1. Create PostgreSQL database:

```bash
# Using psql
createdb weatherdb

# Or using PostgreSQL client
psql -U postgres
CREATE DATABASE weatherdb;
\q
```

2. The database tables will be created automatically when you start the server.

#### Start Redis

```bash
# Windows (if installed via Chocolatey)
redis-server

# Linux/Mac
redis-server

# Or using Docker
docker run -d -p 6379:6379 redis:latest
```

#### Run the Backend

```bash
# From backend directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Configure Environment Variables

The `.env.local` file is already created. Verify it contains:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Run the Frontend

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 📱 Usage

1. **Open the application** at `http://localhost:3000`
2. **Allow location access** for automatic weather detection (optional)
3. **Search for cities** using the search bar
4. **Add favorites** by clicking the star icon
5. **Toggle theme** using the button in the bottom-right corner
6. **View forecasts** by scrolling down

## 🌐 API Endpoints

### Weather Endpoints

- `GET /api/weather/current?lat={lat}&lon={lon}` - Get current weather
- `GET /api/weather/forecast?lat={lat}&lon={lon}` - Get forecast data
- `GET /api/weather/hourly?lat={lat}&lon={lon}` - Get hourly forecast
- `GET /api/weather/historical?lat={lat}&lon={lon}&days={days}` - Get historical data

### Location Endpoints

- `GET /api/locations/search?q={query}` - Search locations
- `GET /api/locations/favorites?user_id={user_id}` - Get favorites
- `POST /api/locations/favorites` - Add favorite
- `DELETE /api/locations/favorites/{id}?user_id={user_id}` - Remove favorite

## 🎨 Design System

The application uses a comprehensive design system with:

- **Color Palette**: Premium gradients and harmonious colors
- **Typography**: Inter and Outfit fonts from Google Fonts
- **Spacing**: Consistent spacing scale (xs to 3xl)
- **Animations**: Smooth transitions and micro-interactions
- **Responsive**: Mobile-first approach

## 🚀 Deployment

### Frontend (Vercel)

1. Push your code to GitHub
2. Import project in Vercel
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL=your-backend-url`
4. Deploy!

### Backend (Render/AWS)

#### Render

1. Create new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy!

#### AWS (EC2)

1. Launch EC2 instance
2. Install dependencies
3. Setup PostgreSQL and Redis
4. Configure environment variables
5. Run with systemd or supervisor

## 📊 Database Schema

### Tables

- **locations** - City/location data
- **weather_history** - Historical weather records
- **user_favorites** - User's favorite locations
- **weather_alerts** - Weather alerts (future feature)

## 🔮 Future Enhancements

- [ ] ML-based weather predictions
- [ ] Interactive weather maps
- [ ] Push notifications for alerts
- [ ] Weather comparison between locations
- [ ] Export weather data
- [ ] Social sharing features
- [ ] Weather widgets

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenWeather API for weather data
- Next.js team for the amazing framework
- FastAPI for the excellent Python framework

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Built with ❤️ using Next.js, FastAPI, and modern web technologies**
