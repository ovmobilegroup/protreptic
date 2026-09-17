# Protreptic Export Routes
from fastapi import APIRouter, Depends, Query, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
import json
import io

from ..database import get_db
from ..models import Figure

router = APIRouter()


@router.get("/export")
async def export_data(
    format: str = Query("json", pattern="^(json|md)$"),
    lang: str = Query("zh", pattern="^(zh|en)$"),
    db: AsyncSession = Depends(get_db),
):
    """Export all scenarios."""
    result = await db.execute(select(Figure))
    figures = result.scalars().all()
    
    data = []
    for f in figures:
        data.append({
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
    
    if format == "json":
        content = json.dumps(data, ensure_ascii=False, indent=2)
        media_type = "application/json"
        filename = f"protreptic_export_{lang}.json"
    else:
        # Markdown format
        lines = [f"# Protreptic Export ({lang.upper()})\n", f"Total: {len(data)} scenarios\n"]
        for item in data:
            lines.append(f"## {item['code']}: {item['name']}\n")
            if item['description']:
                lines.append(f"{item['description']}\n")
            lines.append(f"**Modes**: {', '.join(str(m) for m in item['modes'])}\n")
            if item['reason']:
                lines.append(f"**Reason**: {item['reason']}\n")
            if item['steps']:
                for i, step in enumerate(item['steps'], 1):
                    lines.append(f"{i}. {step}")
            if item['expected']:
                lines.append(f"**Expected**: {item['expected']}\n")
            if item['case']:
                lines.append(f"**Case**: {item['case']}\n")
            lines.append(f"**Era**: {item['era']}\n")
            lines.append(f"**Historical Domains**: {', '.join(item['historical_domains'])}\n")
            lines.append(f"**Thinking Domains**: {', '.join(item['domains'])}\n")
            lines.append(f"**Gender**: {item['gender']}\n")
            lines.append(f"**Ethnicity**: {item['ethnicity']}\n")
            lines.append("---\n")
        content = "\n".join(lines)
        media_type = "text/markdown"
        filename = f"protreptic_export_{lang}.md"
    
    return StreamingResponse(
        io.BytesIO(content.encode("utf-8")),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )