# Protreptic Tags Routes
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any, List, Optional
from ..database import get_db
from ..models import Figure
from ..schemas import StatsResponse

router = APIRouter()


# Predefined tag values
TAG_VALUES = {
    "era": [
        "Pre-Qin", "Qin-Han", "Three-Kingdoms-Jin", "Northern-Southern",
        "Sui-Tang", "Song-Yuan", "Ming-Qing", "Modern-Early", "Modern"
    ],
    "historical_domain": [
        "Military", "Philosophy", "Governance", "Science_Tech", "Historiography",
        "Literature_Arts", "Religion", "Education", "Economics", "Ethics"
    ],
    "domain": [
        "Strategic", "Analytical", "Collaborative", "Operational",
        "Systems", "Creative", "Personal"
    ],
    "gender": ["Male", "Female"],
    "ethnicity": ["Han", "Minority"],
}


@router.get("/stats", response_model=StatsResponse)
async def get_tag_stats(db: AsyncSession = Depends(get_db)):
    """Get tag statistics."""
    stats = {}

    # Era stats
    result = await db.execute(
        select(Figure.era, func.count(Figure.id))
        .where(Figure.era.isnot(None))
        .group_by(Figure.era)
    )
    stats["era"] = {row[0]: row[1] for row in result.all()}

    # Historical domain stats (JSON array)
    result = await db.execute(
        select(Figure.historical_domains)
    )
    hd_counts = {}
    for row in result.all():
        if row[0]:
            for domain in row[0]:
                hd_counts[domain] = hd_counts.get(domain, 0) + 1
    stats["historical_domain"] = hd_counts

    # Domain stats (JSON array)
    result = await db.execute(
        select(Figure.domains)
    )
    d_counts = {}
    for row in result.all():
        if row[0]:
            for domain in row[0]:
                d_counts[domain] = d_counts.get(domain, 0) + 1
    stats["domain"] = d_counts

    # Gender stats
    result = await db.execute(
        select(Figure.gender, func.count(Figure.id))
        .where(Figure.gender.isnot(None))
        .group_by(Figure.gender)
    )
    stats["gender"] = {row[0]: row[1] for row in result.all()}

    # Ethnicity stats
    result = await db.execute(
        select(Figure.ethnicity, func.count(Figure.id))
        .where(Figure.ethnicity.isnot(None))
        .group_by(Figure.ethnicity)
    )
    stats["ethnicity"] = {row[0]: row[1] for row in result.all()}

    # Total
    result = await db.execute(select(func.count(Figure.id)))
    stats["total"] = result.scalar()

    return StatsResponse(data=stats)


@router.get("/values")
async def get_tag_values():
    """Get all available tag values for filter dropdowns."""
    return {"success": True, "data": TAG_VALUES}


@router.get("/filter")
async def filter_figures(
    era: Optional[str] = None,
    historical_domain: Optional[str] = None,
    domain: Optional[str] = None,
    gender: Optional[str] = None,
    ethnicity: Optional[str] = None,
    lang: str = Query("zh", pattern="^(zh|en)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Filter figures by tags."""
    query = select(Figure)
    count_query = select(func.count(Figure.id))

    if era:
        query = query.where(Figure.era == era)
        count_query = count_query.where(Figure.era == era)

    if historical_domain:
        query = query.where(Figure.historical_domains.contains([historical_domain]))
        count_query = count_query.where(Figure.historical_domains.contains([historical_domain]))

    if domain:
        query = query.where(Figure.domains.contains([domain]))
        count_query = count_query.where(Figure.domains.contains([domain]))

    if gender:
        query = query.where(Figure.gender == gender)
        count_query = count_query.where(Figure.gender == gender)

    if ethnicity:
        query = query.where(Figure.ethnicity == ethnicity)
        count_query = count_query.where(Figure.ethnicity == ethnicity)

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    figures = result.scalars().all()

    items = []
    for f in figures:
        items.append({
            "code": f.code,
            "name": f.name_zh if lang == "zh" else f.name_en,
            "description": f.description_zh if lang == "zh" else f.description_en,
            "modes": f.modes,
            "reason": f.reason_zh if lang == "zh" else f.reason_en,
            "steps": f.steps_zh if lang == "zh" else f.steps_en,
            "expected": f.expected_zh if lang == "zh" else f.expected_en,
            "case": f.case_zh if lang == "zh" else f.case_en,
            "era": f.era,
            "historical_domains": f.historical_domains,
            "domains": f.domains,
            "gender": f.gender,
            "ethnicity": f.ethnicity,
        })

    return {
        "success": True,
        "data": items,
        "meta": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "filters_applied": {
                "era": era,
                "historical_domain": historical_domain,
                "domain": domain,
                "gender": gender,
                "ethnicity": ethnicity,
            }
        }
    }