#!/usr/bin/env python3
"""
Data loader for Protreptic API.
Loads scenarios from JSON files into SQLite database.
"""
import json
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, JSON, Index

# Database models (inline for simplicity)
Base = declarative_base()


class Figure(Base):
    __tablename__ = "figures"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    
    # Chinese fields
    name_zh = Column(String(200), nullable=False)
    description_zh = Column(Text)
    reason_zh = Column(Text)
    steps_zh = Column(Text)  # Store as JSON string
    expected_zh = Column(Text)
    case_zh = Column(Text)
    
    # English fields
    name_en = Column(String(200), nullable=False)
    description_en = Column(Text)
    reason_en = Column(Text)
    steps_en = Column(Text)  # Store as JSON string
    expected_en = Column(Text)
    case_en = Column(Text)
    
    # Shared fields
    modes = Column(Text)  # Store as JSON string
    era = Column(String(50))
    historical_domains = Column(Text)  # Store as JSON string
    domains = Column(Text)  # Store as JSON string
    gender = Column(String(20))
    ethnicity = Column(String(20))

    __table_args__ = (
        Index("idx_figure_code", "code"),
        Index("idx_figure_era", "era"),
        Index("idx_figure_gender", "gender"),
        Index("idx_figure_ethnicity", "ethnicity"),
    )


def serialize_field(obj):
    """Serialize any field to JSON string."""
    if obj is None:
        return "[]"
    if isinstance(obj, list):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, str):
        return obj
    return json.dumps(obj, ensure_ascii=False)


async def load_data():
    # Load JSON data
    with open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json', 'r', encoding='utf-8') as f:
        scenarios_zh = json.load(f)
    
    with open('/opt/data/workspace/Protreptic/tools/scenarios_en.json', 'r', encoding='utf-8') as f:
        scenarios_en = json.load(f)
    
    with open('/opt/data/workspace/Protreptic/tools/scenario_tags.json', 'r', encoding='utf-8') as f:
        tags_data = json.load(f)
    
    # Create engine
    engine = create_async_engine("sqlite+aiosqlite:///./protreptic.db", echo=True)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Load data
    tags = tags_data.get('tags', {})
    
    async with async_session_maker() as session:
        count = 0
        for code, zh_data in scenarios_zh.items():
            # Skip non-dict entries (metadata fields)
            if not isinstance(zh_data, dict):
                continue
            en_data = scenarios_en.get(code, {})
            if not isinstance(en_data, dict):
                continue
            tag_data = tags.get(code, {})
            
            if not en_data:
                print(f"Warning: No English data for {code}, skipping")
                continue
            
            figure = Figure(
                code=code,
                # 键接驳（W4 §三，同 tools/build_figures_db.py）: name 优先，回退 name_zh/name_en
                name_zh=zh_data.get('name') or zh_data.get('name_zh') or '',
                name_en=en_data.get('name') or en_data.get('name_en') or '',
                description_zh=serialize_field(zh_data.get('description', '')),
                description_en=serialize_field(en_data.get('description', '')),
                reason_zh=serialize_field(zh_data.get('reason', '')),
                reason_en=serialize_field(en_data.get('reason', '')),
                steps_zh=serialize_field(zh_data.get('steps', [])),
                steps_en=serialize_field(en_data.get('steps', [])),
                expected_zh=serialize_field(zh_data.get('expected', [])),
                expected_en=serialize_field(en_data.get('expected', [])),
                case_zh=serialize_field(zh_data.get('case', '')),
                case_en=serialize_field(en_data.get('case', '')),
                modes=serialize_field(zh_data.get('modes', [])),
                era=tag_data.get('era'),
                historical_domains=serialize_field(tag_data.get('historical_domains', [])),
                domains=serialize_field(tag_data.get('domains', [])),
                gender=tag_data.get('gender'),
                ethnicity=tag_data.get('ethnicity'),
            )
            session.add(figure)
            count += 1
        
        await session.commit()
        print(f"Loaded {count} scenarios into database")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(load_data())