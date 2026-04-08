from fastapi import FastAPI
from app.api.routes import router
from app.core.config import get_settings

# =========================================================
# 📌 Inicialización de la aplicación
# =========================================================
# Cargamos la configuración centralizada (variables de entorno)
# para definir parámetros dinámicos como el nombre de la app.
settings = get_settings()

# =========================================================
# 📌 Creación de la instancia de FastAPI
# =========================================================
# Se instancia la aplicación principal.
#
# Decisión de diseño:
# - Se utiliza configuración externa (settings.app_name)
# - Permite adaptar el comportamiento según entorno (dev/prod)
app = FastAPI(
    title=settings.app_name  # Nombre visible en Swagger (/docs)
)

# =========================================================
# 📌 Registro de rutas
# =========================================================
# Se agregan los endpoints definidos en el router.
#
# Beneficio:
# - Mantiene la aplicación modular
# - Permite escalar agregando múltiples routers
# - Mejora la organización del código
app.include_router(router)