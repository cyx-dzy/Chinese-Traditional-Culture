from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Building, FAQ
from ..schemas import HomeResponse, HomeHighlightBuilding, HomeStats, FAQItem


router = APIRouter(prefix="/home", tags=["home"])


@router.get("/", response_model=HomeResponse)
def get_home_data(db: Session = Depends(get_db)):
    """
    首页需要的综合数据：高亮建筑、统计数据、FAQ 预览。
    """
    # 高亮建筑：每个分类随机取 1 个，如果数据不足就少一些
    categories = ["木结构", "砖石", "园林", "法式"]
    highlights: List[HomeHighlightBuilding] = []
    for cat in categories:
        b = (
            db.query(Building)
            .filter(Building.category == cat)
            .order_by(func.rand())
            .first()
        )
        if b:
            highlights.append(HomeHighlightBuilding.model_validate(b))

    # 统计信息
    total = db.query(func.count(Building.id)).scalar() or 0

    by_category_rows = (
        db.query(Building.category, func.count(Building.id))
        .group_by(Building.category)
        .all()
    )
    by_category = {cat: count for cat, count in by_category_rows}

    by_dynasty_rows = (
        db.query(Building.dynasty, func.count(Building.id))
        .group_by(Building.dynasty)
        .all()
    )
    by_dynasty = {dyn: count for dyn, count in by_dynasty_rows}

    stats = HomeStats(
        total_buildings=total,
        by_category=by_category,
        by_dynasty=by_dynasty,
    )

    # FAQ 预览：取排序靠前的若干条
    faq_rows = (
        db.query(FAQ).order_by(FAQ.sort_order, FAQ.id).limit(5).all()
    )
    faq_preview = [FAQItem.model_validate(row) for row in faq_rows]

    return HomeResponse(
        highlights=highlights,
        stats=stats,
        faq_preview=faq_preview,
    )

