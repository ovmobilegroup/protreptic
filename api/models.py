# Protreptic Database Models
from sqlalchemy import Column, String, Integer, Text, JSON, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Figure(Base):
    __tablename__ = "figures"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    
    # Chinese fields
    name_zh = Column(String(200), nullable=False)
    description_zh = Column(Text)
    reason_zh = Column(Text)
    steps_zh = Column(JSON)
    expected_zh = Column(Text)
    case_zh = Column(Text)
    
    # English fields
    name_en = Column(String(200), nullable=False)
    description_en = Column(Text)
    reason_en = Column(Text)
    steps_en = Column(JSON)
    expected_en = Column(Text)
    case_en = Column(Text)
    
    # Shared fields
    modes = Column(JSON)  # List of mode IDs
    era = Column(String(50))
    historical_domains = Column(JSON)  # List of historical domains
    domains = Column(JSON)  # List of thinking domains
    gender = Column(String(20))
    ethnicity = Column(String(20))

    __table_args__ = (
        Index("idx_figure_code", "code"),
        Index("idx_figure_era", "era"),
        Index("idx_figure_gender", "gender"),
        Index("idx_figure_ethnicity", "ethnicity"),
    )