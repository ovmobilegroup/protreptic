# Protreptic Health Check Route
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ..database import get_db
from ..models import Figure
from ..schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint."""
    # Count figures
    result = await db.execute(select(func.count(Figure.id)))
    total_figures = result.scalar()

    # Count by category
    categories = {}
    for cat in ['A', 'B', 'C', 'D', 'H', 'M']:
        result = await db.execute(
            select(func.count(Figure.id)).where(Figure.code.like(f"{cat}-%"))
        )
        categories[cat] = result.scalar()

    return HealthResponse(
        data={
            "status": "healthy",
            "version": "2.1.0",
            "scenarios_count": total_figures,
            "modes_count": 42,
            "categories": categories,
        }
    )