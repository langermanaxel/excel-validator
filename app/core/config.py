from pydantic_settings import BaseSettings
from functools import lru_cache

# BaseSettings automáticamente lee variables de entorno
# y también puede leer desde un archivo .env
class Settings(BaseSettings):
    app_name: str
    redis_url: str
    database_url: str
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Cacheamos la config (patrón singleton limpio)
@lru_cache
def get_settings() -> Settings:
    return Settings()