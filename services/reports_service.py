from sqlalchemy.ext.asyncio import AsyncSession
from models.demography import Demography
import csv
from io import StringIO
from fastapi import HTTPException, status

class ReportsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def export_demography_csv(self) -> str:
        result = await self.db.execute(Demography.__table__.select())
        rows = result.fetchall()
        if not rows:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data to export")

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(Demography.__table__.columns.keys())
        for row in rows:
            writer.writerow(row)

        csv_content = output.getvalue()
        output.close()
        return csv_content
