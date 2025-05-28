from fastapi import APIRouter, Depends, HTTPException
from core.security import get_current_active_user
from services.gis_service import GISService

router = APIRouter()

@router.get("/schools")
async def fetch_schools_from_gis(
    query: str = "школа",
    region_id: int = 117,
    current_user=Depends(get_current_active_user),
):
    schools = await GISService.fetch_schools(query=query, region_id=region_id)
    if not schools:
        raise HTTPException(status_code=404, detail="Schools not found")
    return schools
