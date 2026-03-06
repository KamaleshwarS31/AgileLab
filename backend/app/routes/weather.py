kfrom fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models.schemas import (
    CurrentWeatherResponse,
    ForecastResponse,
    LocationSearch,
    FavoriteLocation,
    AddFavoriteRequest,
    HistoricalWeatherResponse
)
from app.models.models import Location, WeatherHistory, UserFavorite
from app.services.weather_service import weather_service

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/current", response_model=CurrentWeatherResponse)
async def get_current_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    db: Session = Depends(get_db)
):
    """Get current weather for a location"""
    
    weather = await weather_service.get_current_weather(lat, lon)
    
    if not weather:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    # Store in database for historical tracking
    try:
        # Find or create location
        location = db.query(Location).filter(
            Location.latitude == lat,
            Location.longitude == lon
        ).first()
        
        if not location:
            location = Location(
                name=weather.location,
                country=weather.country,
                latitude=lat,
                longitude=lon
            )
            db.add(location)
            db.commit()
            db.refresh(location)
        
        # Store weather history
        history = WeatherHistory(
            location_id=location.id,
            timestamp=datetime.fromtimestamp(weather.dt),
            temperature=weather.temperature,
            feels_like=weather.feels_like,
            temp_min=weather.temp_min,
            temp_max=weather.temp_max,
            pressure=weather.pressure,
            humidity=weather.humidity,
            wind_speed=weather.wind_speed,
            wind_deg=weather.wind_deg,
            clouds=weather.clouds,
            weather_main=weather.weather.main,
            weather_description=weather.weather.description,
            weather_icon=weather.weather.icon,
            visibility=weather.visibility
        )
        db.add(history)
        db.commit()
        
    except Exception as e:
        print(f"Error storing weather history: {e}")
        db.rollback()
    
    return weather


@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get weather forecast for a location"""
    
    print(f"[ROUTE] Forecast endpoint called with lat={lat}, lon={lon}")
    forecast = await weather_service.get_forecast(lat, lon)
    print(f"[ROUTE] Forecast service returned: {forecast is not None}")
    
    if not forecast:
        print(f"[ROUTE] Forecast is None, returning 404")
        raise HTTPException(status_code=404, detail="Forecast data not found")
    
    print(f"[ROUTE] Returning forecast data")
    return forecast


@router.get("/hourly", response_model=ForecastResponse)
async def get_hourly_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get hourly weather forecast (alias for forecast endpoint)"""
    return await get_forecast(lat, lon)


@router.get("/historical", response_model=List[HistoricalWeatherResponse])
async def get_historical_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    days: int = Query(7, description="Number of days to retrieve", ge=1, le=30),
    db: Session = Depends(get_db)
):
    """Get historical weather data for a location"""
    
    # Find location
    location = db.query(Location).filter(
        Location.latitude == lat,
        Location.longitude == lon
    ).first()
    
    if not location:
        return []
    
    # Get historical data
    start_date = datetime.utcnow() - timedelta(days=days)
    
    history = db.query(WeatherHistory).filter(
        WeatherHistory.location_id == location.id,
        WeatherHistory.timestamp >= start_date
    ).order_by(WeatherHistory.timestamp.desc()).limit(days * 24).all()
    
    return [
        HistoricalWeatherResponse(
            timestamp=h.timestamp,
            temperature=h.temperature,
            feels_like=h.feels_like,
            pressure=h.pressure,
            humidity=h.humidity,
            wind_speed=h.wind_speed,
            weather_main=h.weather_main,
            weather_description=h.weather_description
        )
        for h in history
    ]
