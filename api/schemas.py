# Protreptic Pydantic Schemas
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any


class FigureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
    description: Optional[str] = None
    modes: List[int] = []
    reason: Optional[str] = None
    steps: List[str] = []
    expected: Optional[str] = None
    case: Optional[str] = None
    era: Optional[str] = None
    historical_domains: List[str] = []
    domains: List[str] = []
    gender: Optional[str] = None
    ethnicity: Optional[str] = None


class FigureListResponse(BaseModel):
    success: bool = True
    data: List[FigureResponse]
    meta: Dict[str, Any]


class FigureDetailResponse(BaseModel):
    success: bool = True
    data: FigureResponse


class ModeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    name_en: str
    description: Optional[str] = None
    description_en: Optional[str] = None
    formula: Optional[str] = None
    formula_en: Optional[str] = None
    domain: str
    domain_en: str


class ModeListResponse(BaseModel):
    success: bool = True
    data: List[ModeResponse]


class SearchResponse(BaseModel):
    success: bool = True
    data: List[Dict[str, Any]]
    meta: Dict[str, Any]


class FilterResponse(BaseModel):
    success: bool = True
    data: List[FigureResponse]
    meta: Dict[str, Any]


class StatsResponse(BaseModel):
    success: bool = True
    data: Dict[str, Any]


class HealthResponse(BaseModel):
    success: bool = True
    data: Dict[str, Any]