from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Enum,
    DECIMAL,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship

from database import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    name_en = Column(String(100))
    dynasty = Column(String(50), nullable=False)
    location = Column(String(200))
    category = Column(
        Enum("木结构", "砖石", "园林", "法式", name="building_category"),
        nullable=False,
    )
    summary = Column(Text)
    cover_image = Column(String(500))
    height = Column(DECIMAL(5, 2))
    bay_count = Column(String(20))
    dougong_types = Column(String(50))
    earthquake_resistance = Column(String(50))
    material = Column(String(100))
    preservation_status = Column(String(50))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    details = relationship(
        "BuildingDetail",
        back_populates="building",
        cascade="all, delete-orphan",
        order_by="BuildingDetail.sort_order",
    )
    images = relationship(
        "Image",
        back_populates="building",
        cascade="all, delete-orphan",
        order_by="Image.sort_order",
    )


class BuildingDetail(Base):
    __tablename__ = "building_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    section_type = Column(
        Enum("history", "structure", "material", "culture", name="section_type"),
        nullable=False,
    )
    title = Column(String(200), nullable=False)
    content = Column(Text)
    sort_order = Column(Integer, default=0)

    building = relationship("Building", back_populates="details")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    image_path = Column(String(500), nullable=False)
    image_type = Column(
        Enum("全景", "结构", "斗拱", "彩绘", "其他", name="image_type"),
        default="其他",
    )
    caption = Column(String(200))
    sort_order = Column(Integer, default=0)
    is_cover = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)

    building = relationship("Building", back_populates="images")

    __table_args__ = (Index("idx_building", "building_id"),)


class FAQ(Base):
    __tablename__ = "faq"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String(200), nullable=False)
    answer = Column(Text, nullable=False)
    sort_order = Column(Integer, default=0)

