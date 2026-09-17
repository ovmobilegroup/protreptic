# Protreptic Search Routes
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Dict, Any, Optional
from ..database import get_db
from ..models import Figure
from ..schemas import SearchResponse
from ..semantic_search import create_semantic_search_engine, SemanticSearchEngine

router = APIRouter()


def get_semantic_engine() -> SemanticSearchEngine:
    """Create semantic search engine with latest index (no global caching)."""
    try:
        # Use factory function defaults which resolve to correct absolute paths
        return create_semantic_search_engine()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=f"Semantic search unavailable: {str(e)}")
router = APIRouter()


@router.get("/scenarios/search", response_model=SearchResponse)
async def search_scenarios(
    q: str = Query(..., min_length=1),
    lang: str = Query("zh", pattern="^(zh|en)$"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Keyword search scenarios (exact/substring match)."""
    search_term = f"%{q}%"
    
    query = select(Figure).where(
        or_(
            Figure.name_zh.ilike(search_term),
            Figure.name_en.ilike(search_term),
            Figure.reason_zh.ilike(search_term),
            Figure.reason_en.ilike(search_term),
            Figure.code.ilike(search_term),
            Figure.description_zh.ilike(search_term),
            Figure.description_en.ilike(search_term),
        )
    ).limit(limit)
    
    result = await db.execute(query)
    figures = result.scalars().all()
    
    data = []
    for f in figures:
        data.append({
            "code": f.code,
            "name": f.name_zh if lang == "zh" else f.name_en,
            "match_type": "name" if q.lower() in (f.name_zh.lower() if lang == "zh" else f.name_en.lower()) else "reason"
        })
    
    return SearchResponse(
        data=data,
        meta={"total": len(data), "query": q}
    )


@router.get("/search/semantic")
async def semantic_search_scenarios(
    q: str = Query(..., min_length=1, description="Natural language query"),
    lang: str = Query("zh", pattern="^(zh|en)$"),
    top_k: int = Query(10, ge=1, le=50, description="Number of results"),
    engine: SemanticSearchEngine = Depends(get_semantic_engine),
):
    """
    Semantic search using vector embeddings (BGE-m3 + FAISS).
    
    Finds scenarios semantically similar to the query, not just keyword matches.
    Uses BGE-m3 embeddings + FAISS index for fast similarity search.
    """
    try:
        results, search_time = engine.search(q, top_k=top_k, lang=lang)
        
        # Format for response
        data = []
        for r in results:
            data.append({
                "code": r["code"],
                "name": r["name"],
                "description": r.get("description", ""),
                "reason": r.get("reason", ""),
                "modes": r.get("modes", []),
                "similarity_score": r["score"],
            })
        
        return {
            "success": True,
            "data": data,
            "meta": {
                "total": len(data),
                "query": q,
                "search_type": "semantic",
                "model": "BAAI/bge-m3",
                "search_time_ms": round(search_time * 1000, 2),
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Semantic search error: {str(e)}")


@router.get("/scenarios/{code}/similar")
async def get_similar_scenarios(
    code: str,
    lang: str = Query("zh", pattern="^(zh|en)$"),
    top_k: int = Query(5, ge=1, le=20),
    engine: SemanticSearchEngine = Depends(get_semantic_engine),
):
    """Find scenarios similar to a given figure using semantic similarity."""
    try:
        results, search_time = engine.get_similar(code, top_k=top_k, lang=lang)
        
        data = []
        for r in results:
            data.append({
                "code": r["code"],
                "name": r["name"],
                "description": r.get("description", ""),
                "reason": r.get("reason", ""),
                "modes": r.get("modes", []),
                "similarity_score": r["score"],
            })
        
        return {
            "success": True,
            "data": data,
            "meta": {
                "total": len(data),
                "source_code": code,
                "search_type": "semantic_similarity",
                "search_time_ms": round(search_time * 1000, 2),
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similarity search error: {str(e)}")