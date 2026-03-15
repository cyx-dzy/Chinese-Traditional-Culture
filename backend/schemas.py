from typing import List, Optional

from pydantic import BaseModel


class ImageBase(BaseModel):
    id: int
    image_path: str
    image_type: str
    caption: Optional[str] = None

    class Config:
        from_attributes = True


class BuildingDetailBase(BaseModel):
    id: int
    section_type: str
    title: str
    content: Optional[str] = None

    class Config:
        from_attributes = True


class BuildingBase(BaseModel):
    id: int
    name: str
    name_en: Optional[str] = None
    dynasty: str
    location: Optional[str] = None
    category: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    height: Optional[float] = None
    bay_count: Optional[str] = None
    dougong_types: Optional[str] = None
    earthquake_resistance: Optional[str] = None
    material: Optional[str] = None
    preservation_status: Optional[str] = None

    class Config:
        from_attributes = True


class BuildingListItem(BuildingBase):
    pass


class BuildingDetailResponse(BuildingBase):
    images: List[ImageBase] = []
    details: List[BuildingDetailBase] = []
    related_buildings: List[BuildingBase] = []


class FAQItem(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        from_attributes = True


class HomeHighlightBuilding(BaseModel):
    id: int
    name: str
    name_en: Optional[str] = None
    dynasty: str
    category: str
    cover_image: Optional[str] = None
    summary: Optional[str] = None

    class Config:
        from_attributes = True


class HomeStats(BaseModel):
    total_buildings: int
    by_category: dict
    by_dynasty: dict


class HomeResponse(BaseModel):
    highlights: list[HomeHighlightBuilding]
    stats: HomeStats
    faq_preview: list[FAQItem]

