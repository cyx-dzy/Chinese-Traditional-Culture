from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import FAQ
from ..schemas import FAQItem


router = APIRouter(prefix="/faq", tags=["faq"])


@router.get("/", response_model=List[FAQItem])
def list_faq(db: Session = Depends(get_db)):
    """
    返回全部 FAQ（用于 AI 问答页左侧常见问题按钮）。
    """
    rows = db.query(FAQ).order_by(FAQ.sort_order, FAQ.id).all()
    return [FAQItem.model_validate(r) for r in rows]

