"""
从 CSV 文件导入基础数据到 MySQL。

假定 CSV 文件位于项目根目录：
- buildings.csv
- building_details.csv
- images.csv
- faq.csv
"""

import csv
from pathlib import Path

from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Building, BuildingDetail, Image, FAQ


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def import_buildings(csv_path: Path, db: Session):
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            building = Building(
                id=int(row["id"]) if row.get("id") else None,
                name=row.get("name") or "",
                name_en=row.get("name_en") or None,
                dynasty=row.get("dynasty") or "",
                location=row.get("location") or None,
                category=row.get("category") or "",
                summary=row.get("summary") or None,
                cover_image=row.get("cover_image") or None,
                height=float(row["height"]) if row.get("height") else None,
                bay_count=row.get("bay_count") or None,
                dougong_types=row.get("dougong_types") or None,
                earthquake_resistance=row.get("earthquake_resistance") or None,
                material=row.get("material") or None,
                preservation_status=row.get("preservation_status") or None,
            )
            db.merge(building)
    db.commit()


def import_building_details(csv_path: Path, db: Session):
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            detail = BuildingDetail(
                id=int(row["id"]) if row.get("id") else None,
                building_id=int(row["building_id"]),
                section_type=row.get("section_type") or "history",
                title=row.get("title") or "",
                content=row.get("content") or None,
                sort_order=int(row["sort_order"]) if row.get("sort_order") else 0,
            )
            db.merge(detail)
    db.commit()


def import_images(csv_path: Path, db: Session):
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            image = Image(
                id=int(row["id"]) if row.get("id") else None,
                building_id=int(row["building_id"]),
                image_path=row.get("image_path") or "",
                image_type=row.get("image_type") or "其他",
                caption=row.get("caption") or None,
                sort_order=int(row["sort_order"]) if row.get("sort_order") else 0,
                is_cover=row.get("is_cover", "").strip() in ("1", "true", "True", "YES", "yes"),
            )
            db.merge(image)
    db.commit()


def import_faq(csv_path: Path, db: Session):
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            faq = FAQ(
                id=int(row["id"]) if row.get("id") else None,
                question=row.get("question") or "",
                answer=row.get("answer") or "",
                sort_order=int(row["sort_order"]) if row.get("sort_order") else 0,
            )
            db.merge(faq)
    db.commit()


def main():
    db = SessionLocal()
    try:
        buildings_csv = PROJECT_ROOT / "buildings.csv"
        details_csv = PROJECT_ROOT / "building_details.csv"
        images_csv = PROJECT_ROOT / "images.csv"
        faq_csv = PROJECT_ROOT / "faq.csv"

        if buildings_csv.exists():
            import_buildings(buildings_csv, db)
        if details_csv.exists():
            import_building_details(details_csv, db)
        if images_csv.exists():
            import_images(images_csv, db)
        if faq_csv.exists():
            import_faq(faq_csv, db)
    finally:
        db.close()


if __name__ == "__main__":
    main()

