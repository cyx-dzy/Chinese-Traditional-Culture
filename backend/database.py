from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .config import settings


class Base(DeclarativeBase):
    pass


def get_database_url() -> str:
    """
    Build the SQLAlchemy database URL for MySQL using PyMySQL driver.
    """
    return (
        f"mysql+pymysql://{settings.db_user}:"
        f"{settings.db_password}@{settings.db_host}:"
        f"{settings.db_port}/{settings.db_name}"
        "?charset=utf8mb4"
    )


engine = create_engine(
    get_database_url(),
    echo=settings.debug,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

