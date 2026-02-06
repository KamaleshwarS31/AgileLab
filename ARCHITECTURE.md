# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     (http://localhost:3000)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      NEXT.JS FRONTEND                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  App Router (Next.js 14+)                                │   │
│  │  - page.tsx (Main page)                                  │   │
│  │  - layout.tsx (Root layout)                              │   │
│  │  - globals.css (Design system)                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Components                                              │   │
│  │  - WeatherCard                                           │   │
│  │  - DailyForecast                                         │   │
│  │  - LocationSearch                                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Services                                                │   │
│  │  - API Client (lib/api.ts)                              │   │
│  │  - Utilities (lib/utils.ts)                             │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API
                             │ (http://localhost:8000)
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      FASTAPI BACKEND                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  API Routes                                              │   │
│  │  - /api/weather/* (Weather endpoints)                   │   │
│  │  - /api/locations/* (Location endpoints)                │   │
│  │  - /docs (Swagger documentation)                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Services                                                │   │
│  │  - WeatherService (OpenWeather API integration)         │   │
│  │  - Cache Manager (Redis)                                │   │
│  │  - Database Manager (PostgreSQL)                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Models                                                  │   │
│  │  - SQLAlchemy Models (Database)                         │   │
│  │  - Pydantic Schemas (Validation)                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────┬──────────────────┬──────────────────┬────────────────┘
           │                  │                  │
           │                  │                  │
           ▼                  ▼                  ▼
┌──────────────────┐ ┌──────────────┐ ┌────────────────────┐
│   POSTGRESQL     │ │    REDIS     │ │  OPENWEATHER API   │
│   DATABASE       │ │    CACHE     │ │                    │
│                  │ │              │ │  api.openweather   │
│  - locations     │ │  - Weather   │ │  map.org           │
│  - weather_      │ │    data      │ │                    │
│    history       │ │  - Location  │ │  - Current weather │
│  - user_         │ │    searches  │ │  - Forecasts       │
│    favorites     │ │  - Forecasts │ │  - Location search │
│  - weather_      │ │              │ │                    │
│    alerts        │ │  TTL: 5 min  │ │                    │
└──────────────────┘ └──────────────┘ └────────────────────┘
```

## Data Flow

### 1. Current Weather Request

```
User → Frontend → Backend → Cache Check
                              │
                              ├─ Cache Hit → Return cached data
                              │
                              └─ Cache Miss → OpenWeather API
                                              │
                                              ├─ Store in cache
                                              ├─ Store in database
                                              └─ Return to user
```

### 2. Location Search

```
User types → Frontend → Backend → Cache Check
                                   │
                                   ├─ Cache Hit → Return results
                                   │
                                   └─ Cache Miss → OpenWeather Geo API
                                                   │
                                                   ├─ Cache results
                                                   └─ Return to user
```

### 3. Favorite Location

```
User clicks ⭐ → Frontend → Backend → Database
                                      │
                                      ├─ Check if exists
                                      ├─ Insert/Delete
                                      └─ Return updated list
```

## Component Architecture

### Frontend Components

```
App (page.tsx)
│
├─ Header
│  ├─ Title
│  └─ Subtitle
│
├─ LocationSearch
│  ├─ Search Input
│  ├─ Geolocation Button
│  └─ Results Dropdown
│
├─ WeatherCard
│  ├─ Location Header
│  ├─ Temperature Display
│  ├─ Weather Icon
│  ├─ Details Grid
│  └─ Sun Times
│
├─ DailyForecast
│  └─ Forecast Cards (7 days)
│
├─ Favorites Section
│  └─ Favorite Cards
│
└─ Theme Toggle
```

### Backend Services

```
FastAPI App
│
├─ Weather Routes
│  ├─ GET /current
│  ├─ GET /forecast
│  ├─ GET /hourly
│  └─ GET /historical
│
├─ Location Routes
│  ├─ GET /search
│  ├─ GET /favorites
│  ├─ POST /favorites
│  └─ DELETE /favorites/{id}
│
└─ Services
   ├─ WeatherService
   │  ├─ getCurrentWeather()
   │  ├─ getForecast()
   │  └─ searchLocation()
   │
   ├─ CacheService
   │  ├─ get()
   │  ├─ set()
   │  └─ delete()
   │
   └─ DatabaseService
      ├─ storeWeatherHistory()
      ├─ getFavorites()
      └─ manageFavorites()
```

## Database Schema

```sql
-- Locations Table
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    state VARCHAR,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_location_coords (latitude, longitude),
    INDEX idx_location_name (name)
);

-- Weather History Table
CREATE TABLE weather_history (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    timestamp TIMESTAMP NOT NULL,
    temperature FLOAT NOT NULL,
    feels_like FLOAT NOT NULL,
    temp_min FLOAT NOT NULL,
    temp_max FLOAT NOT NULL,
    pressure INTEGER NOT NULL,
    humidity INTEGER NOT NULL,
    wind_speed FLOAT NOT NULL,
    wind_deg INTEGER NOT NULL,
    clouds INTEGER NOT NULL,
    weather_main VARCHAR NOT NULL,
    weather_description VARCHAR NOT NULL,
    weather_icon VARCHAR NOT NULL,
    rain_1h FLOAT,
    rain_3h FLOAT,
    snow_1h FLOAT,
    snow_3h FLOAT,
    visibility INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_weather_location_time (location_id, timestamp)
);

-- User Favorites Table
CREATE TABLE user_favorites (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    location_id INTEGER REFERENCES locations(id),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE INDEX idx_user_favorites (user_id, location_id)
);

-- Weather Alerts Table (Future)
CREATE TABLE weather_alerts (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    alert_type VARCHAR NOT NULL,
    severity VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_alerts_location_time (location_id, start_time, end_time)
);
```

## Caching Strategy

```
Cache Key Format: {type}:{identifier}

Examples:
- weather:current:40.7128:-74.0060
- weather:forecast:51.5074:-0.1278
- location:search:london

Cache TTL:
- Current weather: 5 minutes (300s)
- Forecast: 10 minutes (600s)
- Location search: 1 hour (3600s)

Cache Invalidation:
- Automatic expiration (TTL)
- Manual clear on data update
```

## Security Layers

```
┌─────────────────────────────────────┐
│  Frontend Security                  │
│  - React XSS protection             │
│  - Environment variables            │
│  - HTTPS in production              │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  API Security                       │
│  - CORS configuration               │
│  - Input validation (Pydantic)      │
│  - Rate limiting (future)           │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  Database Security                  │
│  - SQL injection prevention (ORM)   │
│  - Connection pooling               │
│  - Prepared statements              │
└─────────────────────────────────────┘
```

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     PRODUCTION                            │
│                                                           │
│  ┌────────────────┐         ┌──────────────────┐        │
│  │   VERCEL       │         │   AWS/RENDER     │        │
│  │   (Frontend)   │◄───────►│   (Backend)      │        │
│  │                │  HTTPS  │                  │        │
│  │  - Next.js     │         │  - FastAPI       │        │
│  │  - Static      │         │  - Uvicorn       │        │
│  │    Assets      │         │  - Python        │        │
│  └────────────────┘         └────────┬─────────┘        │
│                                      │                   │
│                              ┌───────┴────────┐          │
│                              │                │          │
│                    ┌─────────▼──────┐  ┌─────▼──────┐   │
│                    │  PostgreSQL    │  │   Redis    │   │
│                    │  (Managed)     │  │  (Managed) │   │
│                    └────────────────┘  └────────────┘   │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## Performance Optimizations

1. **Caching**: Redis for API responses
2. **Database Indexing**: On frequently queried fields
3. **Connection Pooling**: PostgreSQL connection pool
4. **Static Assets**: Optimized in Next.js
5. **Code Splitting**: Automatic in Next.js
6. **Image Optimization**: Next.js Image component ready
7. **API Response**: Gzip compression
8. **Database Queries**: Optimized with indexes

---

This architecture ensures:
✅ Scalability
✅ Performance
✅ Security
✅ Maintainability
✅ Extensibility
