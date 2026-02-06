-- Weather Forecasting System - Supabase Database Setup
-- Run this SQL in Supabase SQL Editor

-- Enable UUID extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create locations table
CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for locations
CREATE INDEX IF NOT EXISTS idx_location_coords ON locations(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_location_name ON locations(name);

-- Create weather_history table
CREATE TABLE IF NOT EXISTS weather_history (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    temperature DOUBLE PRECISION NOT NULL,
    feels_like DOUBLE PRECISION NOT NULL,
    temp_min DOUBLE PRECISION NOT NULL,
    temp_max DOUBLE PRECISION NOT NULL,
    pressure INTEGER NOT NULL,
    humidity INTEGER NOT NULL,
    wind_speed DOUBLE PRECISION NOT NULL,
    wind_deg INTEGER NOT NULL,
    clouds INTEGER NOT NULL,
    weather_main VARCHAR(100) NOT NULL,
    weather_description VARCHAR(255) NOT NULL,
    weather_icon VARCHAR(50) NOT NULL,
    rain_1h DOUBLE PRECISION,
    rain_3h DOUBLE PRECISION,
    snow_1h DOUBLE PRECISION,
    snow_3h DOUBLE PRECISION,
    visibility INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for weather_history
CREATE INDEX IF NOT EXISTS idx_weather_location_time ON weather_history(location_id, timestamp);

-- Create user_favorites table
CREATE TABLE IF NOT EXISTS user_favorites (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    location_id INTEGER REFERENCES locations(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, location_id)
);

-- Create index for user_favorites
CREATE INDEX IF NOT EXISTS idx_user_favorites ON user_favorites(user_id, location_id);

-- Create weather_alerts table (for future use)
CREATE TABLE IF NOT EXISTS weather_alerts (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id) ON DELETE CASCADE,
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for weather_alerts
CREATE INDEX IF NOT EXISTS idx_alerts_location_time ON weather_alerts(location_id, start_time, end_time);

-- Verify tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Success message
SELECT 'Database setup complete! ✅' as status;
