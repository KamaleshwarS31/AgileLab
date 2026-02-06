import httpx
from typing import Optional, List, Dict, Any
from app.config import settings
from app.cache import cache
from app.models.schemas import (
    CurrentWeatherResponse,
    ForecastResponse,
    HourlyForecast,
    DailyForecast,
    WeatherCondition,
    LocationSearch
)


class OpenWeatherService:
    """Service for interacting with OpenWeather API"""
    
    def __init__(self):
        self.api_key = settings.openweather_api_key
        self.base_url = settings.openweather_base_url
        self.onecall_url = settings.openweather_onecall_url
    
    async def get_current_weather(
        self, 
        lat: float, 
        lon: float
    ) -> Optional[CurrentWeatherResponse]:
        """Get current weather for a location"""
        
        # Check cache first
        cache_key = f"weather:current:{lat}:{lon}"
        cached_data = cache.get(cache_key)
        if cached_data:
            try:
                return CurrentWeatherResponse(**cached_data)
            except Exception as e:
                print(f"Error parsing cached current weather data: {e}")
                # Clear bad cache and continue to fetch fresh data
                cache.delete(cache_key)
        
        # Fetch from API
        url = f"{self.base_url}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                # Transform to our schema
                weather_data = {
                    "location": data["name"],
                    "country": data["sys"]["country"],
                    "latitude": data["coord"]["lat"],
                    "longitude": data["coord"]["lon"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "temp_min": data["main"]["temp_min"],
                    "temp_max": data["main"]["temp_max"],
                    "pressure": data["main"]["pressure"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "wind_deg": data["wind"]["deg"],
                    "clouds": data["clouds"]["all"],
                    "visibility": data.get("visibility"),
                    "weather": {
                        "id": data["weather"][0]["id"],
                        "main": data["weather"][0]["main"],
                        "description": data["weather"][0]["description"],
                        "icon": data["weather"][0]["icon"]
                    },
                    "sunrise": data["sys"]["sunrise"],
                    "sunset": data["sys"]["sunset"],
                    "timezone": data["timezone"],
                    "dt": data["dt"]
                }
                
                result = CurrentWeatherResponse(**weather_data)
                
                # Cache the result
                cache.set(cache_key, result.model_dump(), expiration=300)
                
                return result
                
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error fetching current weather: Status {e.response.status_code}")
            print(f"Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"Error fetching current weather: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_forecast(
        self, 
        lat: float, 
        lon: float
    ) -> Optional[ForecastResponse]:
        """Get hourly and daily forecast for a location"""
        
        # Write to file for debugging
        with open("debug.log", "a") as f:
            f.write(f"\n[FORECAST] Starting forecast request for lat={lat}, lon={lon}\n")
        
        print(f"[FORECAST] Starting forecast request for lat={lat}, lon={lon}")
        
        # Check cache first
        cache_key = f"weather:forecast:{lat}:{lon}"
        print(f"[FORECAST] Checking cache with key: {cache_key}")
        with open("debug.log", "a") as f:
            f.write(f"[FORECAST] Checking cache with key: {cache_key}\n")
        
        cached_data = cache.get(cache_key)
        if cached_data:
            print(f"[FORECAST] Found cached data, attempting to parse...")
            with open("debug.log", "a") as f:
                f.write(f"[FORECAST] Found cached data\n")
            try:
                result = ForecastResponse(**cached_data)
                print(f"[FORECAST] Successfully parsed cached data")
                return result
            except Exception as e:
                print(f"[FORECAST] Error parsing cached forecast data: {e}")
                with open("debug.log", "a") as f:
                    f.write(f"[FORECAST] Error parsing cached data: {e}\n")
                # Clear bad cache and continue to fetch fresh data
                cache.delete(cache_key)
        
        print(f"[FORECAST] No valid cache, fetching from API...")
        with open("debug.log", "a") as f:
            f.write(f"[FORECAST] Fetching from API...\n")
        # Note: OneCall API 3.0 requires subscription, using 2.5 forecast endpoint
        url = f"{self.base_url}/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "cnt": 40  # 5 days, 3-hour intervals
        }
        
        try:
            with open("debug.log", "a") as f:
                f.write(f"[FORECAST] Making HTTP request to {url}\n")
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                with open("debug.log", "a") as f:
                    f.write(f"[FORECAST] Got response: {response.status_code}\n")
                response.raise_for_status()
                data = response.json()
                with open("debug.log", "a") as f:
                    f.write(f"[FORECAST] Parsed JSON, got {len(data.get('list', []))} items\n")
                
                # Transform hourly data
                hourly_forecasts = []
                daily_data = {}
                
                for item in data["list"]:
                    # Hourly forecast
                    hourly = HourlyForecast(
                        dt=item["dt"],
                        temperature=item["main"]["temp"],
                        feels_like=item["main"]["feels_like"],
                        pressure=item["main"]["pressure"],
                        humidity=item["main"]["humidity"],
                        clouds=item["clouds"]["all"],
                        wind_speed=item["wind"]["speed"],
                        wind_deg=item["wind"]["deg"],
                        weather=WeatherCondition(
                            id=item["weather"][0]["id"],
                            main=item["weather"][0]["main"],
                            description=item["weather"][0]["description"],
                            icon=item["weather"][0]["icon"]
                        ),
                        pop=item.get("pop", 0),
                        rain=item.get("rain", {}).get("3h"),
                        snow=item.get("snow", {}).get("3h")
                    )
                    hourly_forecasts.append(hourly)
                    
                    # Aggregate daily data
                    from datetime import datetime
                    date = datetime.fromtimestamp(item["dt"]).date()
                    date_str = str(date)
                    
                    if date_str not in daily_data:
                        daily_data[date_str] = {
                            "temps": [],
                            "feels_like": [],
                            "dt": item["dt"],
                            "weather": item["weather"][0],
                            "pressure": item["main"]["pressure"],
                            "humidity": item["main"]["humidity"],
                            "wind_speed": item["wind"]["speed"],
                            "wind_deg": item["wind"]["deg"],
                            "clouds": item["clouds"]["all"],
                            "pop": item.get("pop", 0),
                            "rain": item.get("rain", {}).get("3h", 0),
                            "snow": item.get("snow", {}).get("3h", 0)
                        }
                    
                    daily_data[date_str]["temps"].append(item["main"]["temp"])
                    daily_data[date_str]["feels_like"].append(item["main"]["feels_like"])
                
                # Create daily forecasts
                daily_forecasts = []
                for date_str, day_data in list(daily_data.items())[:7]:
                    temps = day_data["temps"]
                    feels = day_data["feels_like"]
                    
                    daily = DailyForecast(
                        dt=day_data["dt"],
                        sunrise=data["city"]["sunrise"],
                        sunset=data["city"]["sunset"],
                        temp_day=sum(temps) / len(temps),
                        temp_min=min(temps),
                        temp_max=max(temps),
                        temp_night=temps[-1] if temps else temps[0],
                        temp_eve=temps[len(temps)//2] if len(temps) > 1 else temps[0],
                        temp_morn=temps[0],
                        feels_like_day=sum(feels) / len(feels),
                        feels_like_night=feels[-1] if feels else feels[0],
                        feels_like_eve=feels[len(feels)//2] if len(feels) > 1 else feels[0],
                        feels_like_morn=feels[0],
                        pressure=day_data["pressure"],
                        humidity=day_data["humidity"],
                        wind_speed=day_data["wind_speed"],
                        wind_deg=day_data["wind_deg"],
                        clouds=day_data["clouds"],
                        pop=day_data["pop"],
                        rain=day_data["rain"] if day_data["rain"] > 0 else None,
                        snow=day_data["snow"] if day_data["snow"] > 0 else None,
                        weather=WeatherCondition(
                            id=day_data["weather"]["id"],
                            main=day_data["weather"]["main"],
                            description=day_data["weather"]["description"],
                            icon=day_data["weather"]["icon"]
                        ),
                        uvi=None
                    )
                    daily_forecasts.append(daily)
                
                forecast_data = {
                    "latitude": data["city"]["coord"]["lat"],
                    "longitude": data["city"]["coord"]["lon"],
                    "timezone": data["city"]["timezone"],
                    "hourly": [h.model_dump() for h in hourly_forecasts[:48]],  # 48 hours
                    "daily": [d.model_dump() for d in daily_forecasts]
                }
                
                with open("debug.log", "a") as f:
                    f.write(f"[FORECAST] Creating ForecastResponse object...\n")
                result = ForecastResponse(**forecast_data)
                with open("debug.log", "a") as f:
                    f.write(f"[FORECAST] ForecastResponse created successfully!\n")
                
                # Cache the result
                cache.set(cache_key, result.model_dump(), expiration=600)
                
                with open("debug.log", "a") as f:
                    f.write(f"[FORECAST] Returning result\n")
                return result
                
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error fetching forecast: Status {e.response.status_code}")
            print(f"Response: {e.response.text}")
            with open("debug.log", "a") as f:
                f.write(f"[FORECAST] HTTP Error: {e.response.status_code}\n")
            return None
        except KeyError as e:
            print(f"KeyError in forecast data parsing: {e}")
            print(f"This means the API response structure is different than expected")
            with open("debug.log", "a") as f:
                f.write(f"[FORECAST] KeyError: {e}\n")
            import traceback
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"Error fetching forecast: {type(e).__name__}: {e}")
            with open("debug.log", "a") as f:
                f.write(f"[FORECAST] Exception: {type(e).__name__}: {str(e)[:500]}\n")
            import traceback
            traceback.print_exc()
            return None
    
    async def search_location(self, query: str) -> List[LocationSearch]:
        """Search for locations by name"""
        
        # Check cache first
        cache_key = f"location:search:{query.lower()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return [LocationSearch(**loc) for loc in cached_data]
        
        url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": query,
            "limit": 5,
            "appid": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                locations = []
                for item in data:
                    location = LocationSearch(
                        name=item["name"],
                        country=item["country"],
                        state=item.get("state"),
                        latitude=item["lat"],
                        longitude=item["lon"]
                    )
                    locations.append(location)
                
                # Cache the result
                cache.set(cache_key, [loc.model_dump() for loc in locations], expiration=3600)
                
                return locations
                
        except Exception as e:
            print(f"Error searching location: {e}")
            return []


# Singleton instance
weather_service = OpenWeatherService()
