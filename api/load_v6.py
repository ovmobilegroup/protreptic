#!/usr/bin/env python3
"""load_v6.py — 把核心资产 data/modes_data.json（2868 条人物专属模式）
装载进 API 数据库的 thinking_modes 表。

用法（在 api/ 目录、用 protreptic-api venv）：
    python load_v6.py
"""
import json
import asyncio
import sys
from pathlib import Path
from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()
DATA = Path('<repo>/data/modes_data.json')
DB_URL = "sqlite+aiosqlite:///<repo>/api/protreptic.db"


class ThinkingMode(Base):
    __tablename__ = "thinking_modes"

    id = Column(Integer, primary_key=True)
    mode_code = Column(String(64), unique=True, index=True, nullable=False)
    figure_code = Column(String(64), index=True)
    figure_name = Column(String(200), index=True)
    name_zh = Column(String(200))
    name_en = Column(String(200))
    category = Column(String(64), index=True)
    domain_zh = Column(String(200))
    domain_en = Column(String(200))
    definition_zh = Column(Text)
    definition_en = Column(Text)
    process_zh = Column(Text)          # JSON string (list)
    process_en = Column(Text)
    key_concepts = Column(Text)        # JSON string
    source_chapter = Column(Text)
    key_quote_zh = Column(Text)
    representative_cases_zh = Column(Text)   # JSON string
    modern_applications_zh = Column(Text)    # JSON string
    related_modes = Column(Text)             # JSON string
    raw_json = Column(Text)                  # 完整原始记录

    __table_args__ = (
        Index("idx_tm_figure", "figure_code"),
        Index("idx_tm_category", "category"),
    )


def _s(v):
    if v is None:
        return ""
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


async def main():
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    modes = raw.get("modes", [])
    # 去重：mode_code 可能重复（历史遗留），保留首个
    seen = set()
    rows = []
    for m in modes:
        mc = _s(m.get("mode_code"))
        if not mc or mc in seen:
            continue
        seen.add(mc)
        rows.append(m)
    print(f"待装载: {len(rows)} 条（原始 {len(modes)}）")

    engine = create_async_engine(DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with maker() as s:
        # 清空重建
        from sqlalchemy import delete
        await s.execute(delete(ThinkingMode))
        for m in rows:
            s.add(ThinkingMode(
                mode_code=_s(m.get("mode_code")),
                figure_code=_s(m.get("figure_code")),
                figure_name=_s(m.get("figure_name")),
                name_zh=_s(m.get("name_zh")) if not isinstance(m.get("name_zh"), list) else _s(m["name_zh"][0]),
                name_en=_s(m.get("name_en")) if not isinstance(m.get("name_en"), list) else _s(m["name_en"][0]),
                category=_s(m.get("category")),
                domain_zh=_s(m.get("domain_zh")),
                domain_en=_s(m.get("domain_en")),
                definition_zh=_s(m.get("definition_zh")),
                definition_en=_s(m.get("definition_en")),
                process_zh=_s(m.get("process_zh")),
                process_en=_s(m.get("process_en")),
                key_concepts=_s(m.get("key_concepts")),
                source_chapter=_s(m.get("source_chapter")),
                key_quote_zh=_s(m.get("key_quote_zh")),
                representative_cases_zh=_s(m.get("representative_cases_zh")),
                modern_applications_zh=_s(m.get("modern_applications_zh")),
                related_modes=_s(m.get("related_modes")),
                raw_json=json.dumps(m, ensure_ascii=False),
            ))
        await s.commit()

    # 验证
    from sqlalchemy import select, func
    async with maker() as s:
        n = (await s.execute(select(func.count(ThinkingMode.id)))).scalar()
        figs = (await s.execute(select(func.count(func.distinct(ThinkingMode.figure_code))))).scalar()
    print(f"✅ thinking_modes 表: {n} 条, 覆盖 {figs} 个人物")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
