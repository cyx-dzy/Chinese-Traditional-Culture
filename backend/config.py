from pydantic_settings import BaseSettings
import os
import yaml
from pathlib import Path


def load_config():
    config_path = Path(__file__).parent / "config.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


class Settings(BaseSettings):
    app_name: str = "溯光而行"
    debug: bool = True

    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "ancient_building"

    modelscope_api_key: str = ""
    modelscope_model: str = "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
    modelscope_base_url: str = "https://api-inference.modelscope.cn/v1/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        config = load_config()
        
        if config:
            app_config = config.get('app', {})
            db_config = config.get('database', {})
            modelscope_config = config.get('modelscope', {})
            
            if app_config:
                self.app_name = app_config.get('name', self.app_name)
                self.debug = app_config.get('debug', self.debug)
            
            if db_config:
                self.db_host = db_config.get('host', self.db_host)
                self.db_port = db_config.get('port', self.db_port)
                self.db_user = db_config.get('user', self.db_user)
                self.db_password = db_config.get('password', self.db_password)
                self.db_name = db_config.get('name', self.db_name)
            
            if modelscope_config:
                self.modelscope_api_key = modelscope_config.get('api_key', self.modelscope_api_key)
                self.modelscope_model = modelscope_config.get('model', self.modelscope_model)
                self.modelscope_base_url = modelscope_config.get('base_url', self.modelscope_base_url)
        
        if not self.db_password:
            self.db_password = os.environ.get("DB_PASSWORD", "")

    class Config:
        env_file = ".env"


settings = Settings()

