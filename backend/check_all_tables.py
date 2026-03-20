from database import SessionLocal
from models import Building, BuildingDetail, Image, FAQ

db = SessionLocal()

building_count = db.query(Building).count()
detail_count = db.query(BuildingDetail).count()
image_count = db.query(Image).count()
faq_count = db.query(FAQ).count()

print(f'数据库统计:')
print(f'- 建筑表 (buildings): {building_count} 条记录')
print(f'- 建筑详情表 (building_details): {detail_count} 条记录')
print(f'- 图片表 (images): {image_count} 条记录')
print(f'- 常见问题表 (faq): {faq_count} 条记录')

print('\n建筑表前3条记录:')
buildings = db.query(Building).limit(3).all()
for b in buildings:
    print(f'ID: {b.id}, 名称: {b.name}, 朝代: {b.dynasty}')

db.close()