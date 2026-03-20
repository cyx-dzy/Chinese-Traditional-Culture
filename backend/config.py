from pydantic_settings import BaseSettings
import os
import yaml
from pathlib import Path


def load_config():
    config_path = Path(__file__).parent / "config.yaml"
    if not config_path.exists():
        raise RuntimeError(
            f"未找到配置文件：{config_path}\n"
            "请从 config.yaml.example 复制一份为 config.yaml 并填入正确的配置。"
        )
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class Settings(BaseSettings):
    app_name: str = ""
    debug: bool = True

    db_host: str = ""
    db_port: int = 0
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""

    modelscope_api_key: str = ""
    modelscope_model: str = ""
    modelscope_base_url: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        config = load_config()
        
        app_config = config.get('app', {})
        db_config = config.get('database', {})
        modelscope_config = config.get('modelscope', {})
        
        self.app_name = app_config.get('name', '溯光而行')
        self.debug = app_config.get('debug', True)
        
        self.db_host = db_config.get('host', '')
        self.db_port = db_config.get('port', 3306)
        self.db_user = db_config.get('user', '')
        self.db_password = db_config.get('password', '')
        self.db_name = db_config.get('name', '')
        
        self.modelscope_api_key = modelscope_config.get('api_key', '')
        self.modelscope_model = modelscope_config.get('model', 'deepseek-ai/DeepSeek-R1-Distill-Qwen-14B')
        self.modelscope_base_url = modelscope_config.get('base_url', 'https://api-inference.modelscope.cn/v1/')
        
        if not self.db_password:
            self.db_password = os.environ.get("DB_PASSWORD", "")

    class Config:
        env_file = ".env"


settings = Settings()

