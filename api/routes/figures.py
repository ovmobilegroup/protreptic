# Protreptic Figures Routes
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional, List
import math

from ..database import get_db
from ..models import Figure
from ..schemas import FigureResponse, FigureListResponse, FigureDetailResponse


router = APIRouter()


@router.get("", response_model=FigureListResponse)
async def list_figures(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    lang: str = Query("zh", pattern="^(zh|en)$"),
    category: Optional[str] = Query(None, pattern="^(A|B|C|D|H|M)$"),
    search: Optional[str] = None,
    era: Optional[str] = None,
    domain: Optional[str] = None,
    historical_domain: Optional[str] = None,
    gender: Optional[str] = None,
    ethnicity: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List figures with pagination and filtering."""
    query = select(Figure)
    count_query = select(func.count(Figure.id))

    # Category filter (prefix)
    if category:
        query = query.where(Figure.code.like(f"{category}-%"))
        count_query = count_query.where(Figure.code.like(f"{category}-%"))

    # Search
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Figure.name_zh.ilike(search_term),
                Figure.name_en.ilike(search_term),
                Figure.reason_zh.ilike(search_term),
                Figure.reason_en.ilike(search_term),
                Figure.code.ilike(search_term),
            )
        )
        count_query = count_query.where(
            or_(
                Figure.name_zh.ilike(search_term),
                Figure.name_en.ilike(search_term),
                Figure.reason_zh.ilike(search_term),
                Figure.reason_en.ilike(search_term),
                Figure.code.ilike(search_term),
            )
        )

    # Tag filters
    if era:
        query = query.where(Figure.era == era)
        count_query = count_query.where(Figure.era == era)

    if domain:
        query = query.where(Figure.domains.contains([domain]))
        count_query = count_query.where(Figure.domains.contains([domain]))

    if historical_domain:
        query = query.where(Figure.historical_domains.contains([historical_domain]))
        count_query = count_query.where(Figure.historical_domains.contains([historical_domain]))

    if gender:
        query = query.where(Figure.gender == gender)
        count_query = count_query.where(Figure.gender == gender)

    if ethnicity:
        query = query.where(Figure.ethnicity == ethnicity)
        count_query = count_query.where(Figure.ethnicity == ethnicity)

    # Total count
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Pagination
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    figures = result.scalars().all()

    # Convert to response model
    items = []
    for f in figures:
        items.append(
            FigureResponse(
                code=f.code,
                name=f.name_zh if lang == "zh" else f.name_en,
                description=f.description_zh if lang == "zh" else f.description_en,
                modes=f.modes,
                reason=f.reason_zh if lang == "zh" else f.reason_en,
                steps=f.steps_zh if lang == "zh" else f.steps_en,
                expected=f.expected_zh if lang == "zh" else f.expected_en,
                case=f.case_zh if lang == "zh" else f.case_en,
                era=f.era,
                historical_domains=f.historical_domains,
                domains=f.domains,
                gender=f.gender,
                ethnicity=f.ethnicity,
            )
        )

    return FigureListResponse(
        success=True,
        data=items,
        meta={
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": math.ceil(total / page_size),
        },
    )


@router.get("/{code}", response_model=FigureDetailResponse)
async def get_figure(
    code: str,
    lang: str = Query("zh", pattern="^(zh|en)$"),
    db: AsyncSession = Depends(get_db),
):
    """Get a single figure by code."""
    result = await db.execute(select(Figure).where(Figure.code == code.upper()))
    figure = result.scalar_one_or_none()

    if not figure:
        raise HTTPException(status_code=404, detail="Figure not found")

    return FigureDetailResponse(
        success=True,
        data=FigureResponse(
            code=figure.code,
            name=figure.name_zh if lang == "zh" else figure.name_en,
            description=figure.description_zh if lang == "zh" else figure.description_en,
            modes=figure.modes,
            reason=figure.reason_zh if lang == "zh" else figure.reason_en,
            steps=figure.steps_zh if lang == "zh" else figure.steps_en,
            expected=figure.expected_zh if lang == "zh" else figure.expected_en,
            case=figure.case_zh if lang == "zh" else figure.case_en,
            era=figure.era,
            historical_domains=figure.historical_domains,
            domains=figure.domains,
            gender=figure.gender,
            ethnicity=figure.ethnicity,
        ),
    )