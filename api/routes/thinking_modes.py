# Protreptic Thinking Modes (v6 asset) Routes
# 核心资产 2868 条人物专属思维模式的查询接口
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
import json

from ..database import get_db
from ..load_v6 import ThinkingMode

router = APIRouter()


def _row_to_dict(r: ThinkingMode):
    def j(v):
        if not v:
            return []
        try:
            return json.loads(v)
        except Exception:
            return v
    return {
        "mode_code": r.mode_code,
        "figure_code": r.figure_code,
        "figure_name": r.figure_name,
        "name_zh": r.name_zh,
        "name_en": r.name_en,
        "category": r.category,
        "domain_zh": r.domain_zh,
        "domain_en": r.domain_en,
        "definition_zh": r.definition_zh,
        "definition_en": r.definition_en,
        "process_zh": j(r.process_zh),
        "process_en": j(r.process_en),
        "key_concepts": j(r.key_concepts),
        "source_chapter": r.source_chapter,
        "key_quote_zh": r.key_quote_zh,
        "representative_cases_zh": j(r.representative_cases_zh),
        "modern_applications_zh": j(r.modern_applications_zh),
        "related_modes": j(r.related_modes),
    }


@router.get("/thinking-modes")
async def list_modes(
    db: AsyncSession = Depends(get_db),
    category: str | None = Query(None),
    figure: str | None = Query(None),
    q: str | None = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0),
):
    """列出/筛选思维模式（按类目/人物/关键词）。"""
    stmt = select(ThinkingMode)
    if category:
        stmt = stmt.where(ThinkingMode.category == category)
    if figure:
        stmt = stmt.where(ThinkingMode.figure_code == figure.upper())
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(
            ThinkingMode.name_zh.like(like),
            ThinkingMode.definition_zh.like(like),
            ThinkingMode.category.like(like),
            ThinkingMode.domain_zh.like(like),
        ))
    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar()
    rows = (await db.execute(stmt.limit(limit).offset(offset))).scalars().all()
    return {
        "success": True,
        "data": [_row_to_dict(r) for r in rows],
        "meta": {"total": total, "limit": limit, "offset": offset},
    }


@router.get("/thinking-modes/stats")
async def stats(db: AsyncSession = Depends(get_db)):
    """库统计：总数、人物数、类目分布。"""
    total = (await db.execute(select(func.count(ThinkingMode.id)))).scalar()
    figs = (await db.execute(select(func.count(func.distinct(ThinkingMode.figure_code))))).scalar()
    cat_rows = (await db.execute(
        select(ThinkingMode.category, func.count(ThinkingMode.id)).group_by(ThinkingMode.category)
    )).all()
    return {
        "success": True,
        "data": {
            "total_modes": total,
            "total_figures": figs,
            "categories": {c or "?": n for c, n in cat_rows},
        },
    }


@router.get("/figures/{code}/modes")
async def figure_modes(code: str, db: AsyncSession = Depends(get_db)):
    """取某位历史人物的全部思维模式。"""
    up = code.upper()
    rows = (await db.execute(
        select(ThinkingMode).where(func.upper(ThinkingMode.figure_code) == up)
    )).scalars().all()
    if not rows:
        raise HTTPException(status_code=404, detail=f"Figure not found: {code}")
    name = rows[0].figure_name
    return {
        "success": True,
        "data": {
            "figure_code": rows[0].figure_code,
            "figure_name": name,
            "count": len(rows),
            "modes": [_row_to_dict(r) for r in rows],
        },
    }


@router.get("/thinking-modes/{mode_code}")
async def get_mode(mode_code: str, db: AsyncSession = Depends(get_db)):
    """取单条思维模式详情。"""
    r = (await db.execute(
        select(ThinkingMode).where(func.upper(ThinkingMode.mode_code) == mode_code.upper())
    )).scalars().first()
    if not r:
        raise HTTPException(status_code=404, detail=f"Mode not found: {mode_code}")
    return {"success": True, "data": _row_to_dict(r)}
