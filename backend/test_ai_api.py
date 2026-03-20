from database import SessionLocal
from models import FAQ

db = SessionLocal()

count = db.query(FAQ).count()
print(f'FAQ表中共有 {count} 条记录')

if count > 0:
    print('\n前3条记录:')
    faqs = db.query(FAQ).limit(3).all()
    for f in faqs:
        print(f'ID: {f.id}, 问题: {f.question[:50]}...')
else:
    print('FAQ表中没有数据')

db.close()