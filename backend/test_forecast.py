import httpx
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

async def test_forecast():
    api_key = os.getenv('OPENWEATHER_API_KEY')
    print(f"Testing forecast API with key: {api_key[:10]}...")
    
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": 12.97,
        "lon": 79.16,
        "appid": api_key,
        "units": "metric",
        "cnt": 40
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Success! Got {len(data.get('list', []))} forecast items")
                print(f"City: {data.get('city', {}).get('name')}")
            else:
                print(f"Error Response: {response.text[:500]}")
        except Exception as e:
            print(f"Exception: {e}")

asyncio.run(test_forecast())
