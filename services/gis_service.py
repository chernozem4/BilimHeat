import os
import httpx
from fastapi import HTTPException

API_2GIS_KEY = os.getenv("API_2GIS_KEY")
BASE_URL_2GIS = "https://catalog.api.2gis.com/3.0/items"

class GISService:
    @staticmethod
    async def fetch_schools(query: str = "школа", region_id: int = 117, limit: int = 10):
        if not API_2GIS_KEY:
            raise HTTPException(status_code=500, detail="2GIS API key not configured")

        params = {
            "q": query,
            "region_id": region_id,
            "key": API_2GIS_KEY,
            "fields": "items.point,items.address_name",
            "limit": limit,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL_2GIS, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error fetching data from 2GIS")

        data = response.json()
        items = data.get("result", {}).get("items", [])
        schools = []
        for item in items:
            schools.append({
                "name": item.get("name"),
                "address": item.get("address_name"),
                "location": item.get("point")
            })
        return schools
