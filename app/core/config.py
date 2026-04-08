from pydantic_settings import BaseSettings
from functools import lru_cache


# =========================================================
# 📌 Clase de configuración de la aplicación
# =========================================================
# Esta clase centraliza todas las variables de configuración
# de la aplicación (ej: URLs, nombres, niveles de log, etc.).
#
# BaseSettings (de pydantic-settings):
# - Lee automáticamente variables de entorno
# - Permite tipado fuerte (evita errores en runtime)
# - Facilita validación y mantenimiento
#
# Beneficio:
# - Evita hardcodear valores sensibles
# - Permite cambiar configuración sin modificar código
# =========================================================
class Settings(BaseSettings):

    # Nombre de la aplicación (usado en FastAPI, logs, etc.)
    app_name: str

    # URL de Redis (usado como broker y backend en Celery)
    redis_url: str

    # URL de la base de datos
    database_url: str

    # Nivel de logging (por defecto INFO)
    log_level: str = "INFO"

    # -----------------------------------------------------
    # Configuración interna de Pydantic
    # -----------------------------------------------------
    # Define que las variables se pueden cargar desde un archivo .env
    # Esto es útil en desarrollo y testing
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# =========================================================
# 📌 Función de acceso a configuración (Singleton)
# =========================================================
# Se utiliza lru_cache para evitar recrear la configuración
# múltiples veces durante la ejecución.
#
# Beneficios:
# - Mejora performance (se instancia una sola vez)
# - Garantiza consistencia en toda la app
# - Implementa un patrón tipo Singleton de forma simple
# =========================================================
@lru_cache
def get_settings() -> Settings:
    return Settings()