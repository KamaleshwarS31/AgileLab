# Backend - FastAPI Weather API

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Setup environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Start PostgreSQL and Redis

4. Run the server:
```bash
python -m uvicorn app.main:app --reload
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration
│   ├── database.py       # Database connection
│   ├── cache.py          # Redis cache
│   ├── models/           # Database models & schemas
│   ├── routes/           # API endpoints
│   └── services/         # Business logic
├── requirements.txt      # Python dependencies
└── .env.example         # Environment template
```

## Environment Variables

- `OPENWEATHER_API_KEY` - Your OpenWeather API key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `CORS_ORIGINS` - Allowed CORS origins
- `SECRET_KEY` - Secret key for security
- `CACHE_EXPIRATION` - Cache expiration time (seconds)

## Testing

```bash
# Run tests (when implemented)
pytest
```

## Deployment

See main README for deployment instructions.
