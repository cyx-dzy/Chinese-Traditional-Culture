from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import buildings, home, faq, ai
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="中国古代建筑成就数字展 后端接口",
    version="0.1.0",
)

logger.info(f"启动 {settings.app_name} 后端服务")
logger.info(f"调试模式: {settings.debug}")
logger.info(f"数据库: {settings.db_user}@{settings.db_host}:{settings.db_port}/{settings.db_name}")

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
app.include_router(ai.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

