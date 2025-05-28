from fastapi import APIRouter, Depends, HTTPException
from core.security import get_current_active_user
from typing import List
import httpx
import os

router = APIRouter()

API_2GIS_KEY = os.getenv("API_2GIS_KEY")
BASE_URL_2GIS = "https://catalog.api.2gis.com/3.0/items"

@router.get("/schools")
async def fetch_schools_from_2gis(
    q: str = "школа",
    region_id: int = 117,
    current_user=Depends(get_current_active_user),
):
    """
    Fetch schools data from external 2GIS API with caching considerations.
    """
    if not API_2GIS_KEY:
        raise HTTPException(status_code=500, detail="2GIS API key not configured")

    params = {
        "q": q,
        "region_id": region_id,
        "key": API_2GIS_KEY,
        "fields": "items.point,items.address_name",
        "limit": 10,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL_2GIS, params=params)

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"2GIS API request failed with status code {response.status_code}"
        )

    data = response.json()
    schools = [
        {
            "name": item.get("name"),
            "address": item.get("address_name"),
            "location": item.get("point"),
        }
        for item in data.get("result", {}).get("items", [])
    ]

    return schools
