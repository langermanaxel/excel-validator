import logging
from app.core.config import get_settings

# =========================================================
# 📌 Configuración de logging
# =========================================================
# Obtenemos la configuración centralizada de la app,
# lo que permite definir el nivel de logs desde variables
# de entorno (ej: INFO, DEBUG, ERROR)
settings = get_settings()


# =========================================================
# 📌 Factory de loggers
# =========================================================
# Esta función devuelve un logger configurado para el módulo
# que lo solicite.
#
# Decisiones de diseño:
# - Se centraliza la configuración del logging
# - Se evita duplicar configuración en múltiples archivos
# - Se permite cambiar nivel de logs sin modificar código
#
# Parámetros:
# - name: nombre del logger (generalmente __name__)
#
# Retorna:
# - Instancia de logging.Logger lista para usar
# =========================================================
def get_logger(name: str) -> logging.Logger:

    # Configuración base del sistema de logging
    logging.basicConfig(
        # Archivo donde se guardan los logs
        filename="app.log",

        # Nivel de logging (INFO, DEBUG, etc.)
        # Se controla desde variables de entorno
        level=settings.log_level,

        # Formato del log:
        # - timestamp
        # - nivel (INFO, ERROR, etc.)
        # - mensaje
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Retornamos un logger asociado al módulo que lo invoca
    return logging.getLogger(name)