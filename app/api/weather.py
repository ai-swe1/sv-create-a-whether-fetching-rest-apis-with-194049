from fastapi import APIRouter, HTTPException
import json
import sqlite3
import urllib.parse
import urllib.request
import urllib.error

weather_router = APIRouter()


@weather_router.get("/weather")
async def get_weather(city: str | None = None):
    """Retrieve weather information for a given city.

    - Missing *city* query parameter → 400 Bad Request
    - City not found in external service → 404 Not Found
    - External service failure (network/HTTP error) → 502 Bad Gateway
    - Any unexpected error → 500 Internal Server Error
    """
    try:
        # 1️⃣ Validate request
        if not city:
            raise HTTPException(status_code=400, detail="Missing required query parameter: city")

        # 2️⃣ Call external weather API (placeholder URL)
        encoded_city = urllib.parse.quote(city)
        api_url = f"https://api.example.com/weather?city={encoded_city}"
        try:
            with urllib.request.urlopen(api_url, timeout=5) as response:
                if response.status != 200:
                    raise HTTPException(status_code=502, detail="External weather service error")
                raw_body = response.read()
        except urllib.error.URLError as exc:
            raise HTTPException(status_code=502, detail="External weather service unreachable") from exc

        # 3️⃣ Parse JSON response
        try:
            weather_data = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=502, detail="Invalid JSON from external service") from exc

        # 4️⃣ Detect unknown city
        # Assuming the external API returns a field "weather" when successful
        if not weather_data.get("weather"):
            raise HTTPException(status_code=404, detail="City not found")

        # 5️⃣ Cache result in SQLite (using json.dumps for safety)
        conn = sqlite3.connect("weather.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_cache (
                city TEXT PRIMARY KEY,
                data TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            "INSERT OR REPLACE INTO weather_cache (city, data) VALUES (?, ?)",
            (city, json.dumps(weather_data))
        )
        conn.commit()
        conn.close()

        return weather_data

    except HTTPException:
        # Re‑raise known HTTP errors unchanged
        raise
    except Exception as exc:
        # Catch‑all for unexpected failures
        raise HTTPException(status_code=500, detail="Internal server error") from exc
