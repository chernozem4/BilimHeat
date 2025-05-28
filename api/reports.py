from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import get_current_active_user
from database import get_db
from services.reports_service import ReportsService

router = APIRouter()

@router.get("/demography/csv", status_code=status.HTTP_200_OK)
async def export_demography_csv(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = ReportsService(db)
    csv_content = await service.export_demography_csv()
    headers = {"Content-Disposition": "attachment; filename=demography.csv"}
    return Response(content=csv_content, media_type="text/csv", headers=headers)
