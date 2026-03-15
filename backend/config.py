from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Ancient Building Backend"
    debug: bool = True

    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "135792468aB."
    db_name: str = "ancient_building"

    class Config:
        env_file = ".env"


settings = Settings()

