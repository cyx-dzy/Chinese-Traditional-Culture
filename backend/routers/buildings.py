from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Building, BuildingDetail, Image
from ..schemas import BuildingListItem, BuildingDetailResponse, BuildingBase


router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("/", response_model=List[BuildingListItem])
def list_buildings(
    category: Optional[str] = Query(None, description="建筑分类"),
    dynasty: Optional[str] = Query(None, description="朝代筛选"),
    keyword: Optional[str] = Query(None, description="名称或简介关键字"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    获取建筑列表（用于分类页、搜索等）。
    """
    query = db.query(Building)

    if category:
        query = query.filter(Building.category == category)
    if dynasty:
        query = query.filter(Building.dynasty == dynasty)
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(
            (Building.name.like(like))
            | (Building.name_en.like(like))
            | (Building.summary.like(like))
        )

    buildings = (
        query.order_by(Building.dynasty, Building.name).offset(skip).limit(limit).all()
    )
    return buildings


@router.get("/{building_id}", response_model=BuildingDetailResponse)
def get_building_detail(
    building_id: int,
    db: Session = Depends(get_db),
):
    """
    获取单个建筑的完整详情（详情页用）。
    """
    building: Optional[Building] = db.query(Building).filter(
        Building.id == building_id
    ).first()
    if not building:
        raise HTTPException(status_code=404, detail="建筑不存在")

    images = (
        db.query(Image)
        .filter(Image.building_id == building_id)
        .order_by(Image.sort_order)
        .all()
    )
    details = (
        db.query(BuildingDetail)
        .filter(BuildingDetail.building_id == building_id)
        .order_by(BuildingDetail.sort_order)
        .all()
    )

    related = (
        db.query(Building)
        .filter(
            Building.id != building_id,
            (
                (Building.dynasty == building.dynasty)
                | (Building.category == building.category)
            ),
        )
        .order_by(func.rand())
        .limit(3)
        .all()
    )

    return BuildingDetailResponse(
        **BuildingBase.model_validate(building).model_dump(),
        images=images,
        details=details,
        related_buildings=related,
    )

