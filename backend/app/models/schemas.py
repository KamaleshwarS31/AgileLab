from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WeatherCondition(BaseModel):
    """Weather condition schema"""
    id: int
    main: str
    description: str
    icon: str


class CurrentWeatherResponse(BaseModel):
    """Current weather response schema"""
    location: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    wind_speed: float
    wind_deg: int
    clouds: int
    visibility: Optional[int] = None
    weather: WeatherCondition
    sunrise: int
    sunset: int
    timezone: int
    dt: int


class HourlyForecast(BaseModel):
    """Hourly forecast item schema"""
    dt: int
    temperature: float
    feels_like: float
    pressure: int
    humidity: int
    clouds: int
    wind_speed: float
    wind_deg: int
    weather: WeatherCondition
    pop: float  # Probability of precipitation
    rain: Optional[float] = None
    snow: Optional[float] = None


class DailyForecast(BaseModel):
    """Daily forecast item schema"""
    dt: int
    sunrise: int
    sunset: int
    temp_day: float
    temp_min: float
    temp_max: float
    temp_night: float
    temp_eve: float
    temp_morn: float
    feels_like_day: float
    feels_like_night: float
    feels_like_eve: float
    feels_like_morn: float
    pressure: int
    humidity: int
    wind_speed: float
    wind_deg: int
    clouds: int
    pop: float
    rain: Optional[float] = None
    snow: Optional[float] = None
    weather: WeatherCondition
    uvi: Optional[float] = None


class ForecastResponse(BaseModel):
    """Forecast response schema"""
    latitude: float
    longitude: float
    timezone: int  # OpenWeather API returns timezone as integer (seconds offset from UTC)
    hourly: List[HourlyForecast]
    daily: List[DailyForecast]


class LocationSearch(BaseModel):
    """Location search result schema"""
    name: str
    country: str
    state: Optional[str] = None
    latitude: float
    longitude: float


class FavoriteLocation(BaseModel):
    """Favorite location schema"""
    id: int
    location_id: int
    location_name: str
    country: str
    latitude: float
    longitude: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class AddFavoriteRequest(BaseModel):
    """Add favorite location request"""
    user_id: str
    location_name: str
    country: str
    latitude: float
    longitude: float
    state: Optional[str] = None


class WeatherAlertResponse(BaseModel):
    """Weather alert response schema"""
    id: int
    alert_type: str
    severity: str
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    
    class Config:
        from_attributes = True


class HistoricalWeatherResponse(BaseModel):
    """Historical weather response schema"""
    timestamp: datetime
    temperature: float
    feels_like: float
    pressure: int
    humidity: int
    wind_speed: float
    weather_main: str
    weather_description: str
    
    class Config:
        from_attributes = True


class MLPredictionResponse(BaseModel):
    """ML prediction response schema"""
    predicted_temperature: float
    confidence: float
    prediction_date: str
    model_accuracy: Optional[float] = None
