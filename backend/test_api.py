import httpx
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

async def test_api():
    api_key = os.getenv('OPENWEATHER_API_KEY')
    print(f"Testing API key: {api_key[:10]}...")
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": 40.7128,
        "lon": -74.0060,
        "appid": api_key,
        "units": "metric"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text[:500]}")
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(test_api())
