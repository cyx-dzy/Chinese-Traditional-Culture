from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    app_name: str = "溯光而行"
    debug: bool = True

    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "135792468aB."
    db_name: str = "ancient_building"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.db_password:
            self.db_password = os.environ.get("DB_PASSWORD", "")

    class Config:
        env_file = ".env"


settings = Settings()

