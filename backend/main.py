from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import buildings, home, faq


app = FastAPI(
    title=settings.app_name,
    description="中国古代建筑成就数字展 后端接口",
    version="0.1.0",
)

# CORS，方便前端本地调试
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home.router)
app.include_router(buildings.router)
app.include_router(faq.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

