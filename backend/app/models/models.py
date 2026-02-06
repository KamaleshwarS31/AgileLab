from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Location(Base):
    """Location model for storing city/location data"""
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    state = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    weather_history = relationship("WeatherHistory", back_populates="location")
    favorites = relationship("UserFavorite", back_populates="location")
    
    # Indexes
    __table_args__ = (
        Index('idx_location_coords', 'latitude', 'longitude'),
        Index('idx_location_name', 'name'),
    )


class WeatherHistory(Base):
    """Weather history model for storing historical weather data"""
    __tablename__ = "weather_history"
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Weather data
    temperature = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    temp_min = Column(Float, nullable=False)
    temp_max = Column(Float, nullable=False)
    pressure = Column(Integer, nullable=False)
    humidity = Column(Integer, nullable=False)
    wind_speed = Column(Float, nullable=False)
    wind_deg = Column(Integer, nullable=False)
    clouds = Column(Integer, nullable=False)
    weather_main = Column(String, nullable=False)
    weather_description = Column(String, nullable=False)
    weather_icon = Column(String, nullable=False)
    
    # Optional fields
    rain_1h = Column(Float, nullable=True)
    rain_3h = Column(Float, nullable=True)
    snow_1h = Column(Float, nullable=True)
    snow_3h = Column(Float, nullable=True)
    visibility = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    location = relationship("Location", back_populates="weather_history")
    
    # Indexes
    __table_args__ = (
        Index('idx_weather_location_time', 'location_id', 'timestamp'),
    )


class UserFavorite(Base):
    """User favorite locations model"""
    __tablename__ = "user_favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)  # Can be session ID or user ID
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    location = relationship("Location", back_populates="favorites")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_favorites', 'user_id', 'location_id', unique=True),
    )


class WeatherAlert(Base):
    """Weather alerts model"""
    __tablename__ = "weather_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    alert_type = Column(String, nullable=False)  # e.g., "storm", "heat", "cold"
    severity = Column(String, nullable=False)  # e.g., "low", "medium", "high", "extreme"
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_alerts_location_time', 'location_id', 'start_time', 'end_time'),
    )
