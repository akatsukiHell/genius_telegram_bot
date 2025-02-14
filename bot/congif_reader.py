from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    bot_token: SecretStr
    admin_ids: List[str]
    bot_language: str

    
    model_config = SettingsConfigDict(env_file= '.env', env_file_encoding= 'utc-8')

config = Settings()