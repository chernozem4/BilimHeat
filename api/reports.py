from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import get_current_active_user
from database import get_db
from models.demography import Demography
import csv
from io import StringIO

router = APIRouter()


@router.get("/demography/csv", status_code=status.HTTP_200_OK)
async def export_demography_csv(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Экспорт демографических данных в CSV.
    """
    query = await db.execute(Demography.__table__.select())
    rows = query.fetchall()

    if not rows:
        return Response(status_code=status.HTTP_204_NO_CONTENT, content="Нет данных для экспорта")

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(Demography.__table__.columns.keys())
    for row in rows:
        writer.writerow(row)

    csv_content = output.getvalue()
    output.close()

    headers = {"Content-Disposition": "attachment; filename=demography.csv"}
    return Response(content=csv_content, media_type="text/csv", headers=headers)
