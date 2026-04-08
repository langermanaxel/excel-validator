from celery import Celery
from app.core.config import get_settings

# Obtenemos la configuración centralizada de la aplicación
# (variables de entorno como REDIS_URL, etc.)
settings = get_settings()

# =========================================================
# 📌 Inicialización de Celery
# =========================================================
# Celery es el componente encargado de ejecutar tareas en
# segundo plano (asincrónicas), desacoplando el procesamiento
# pesado de la API principal.
#
# Decisiones de diseño:
# - Se utiliza Redis como broker (cola de mensajes)
# - Se utiliza Redis también como backend de resultados
#   para poder consultar el estado de las tareas
# - Se centraliza la configuración usando variables de entorno
#   para facilitar despliegue en distintos entornos (dev/prod)
# =========================================================
celery_app = Celery(
    # Nombre lógico de la aplicación Celery
    # (usado internamente para identificación)
    "worker",

    # Broker: define el sistema de colas donde se envían las tareas
    # Redis actúa como intermediario entre la API y los workers
    broker=settings.redis_url,

    # Backend: almacena el resultado de las tareas ejecutadas
    # Esto permite consultar estados como SUCCESS, FAILURE, etc.
    backend=settings.redis_url
)


# =========================================================
# 📌 Configuración adicional (opcional pero recomendable)
# =========================================================
# Se pueden agregar configuraciones para mejorar comportamiento,
# performance y trazabilidad del sistema.
#
# Ejemplos:
# - Serialización en JSON (interoperabilidad)
# - Timezone consistente
# - Control de reintentos
# =========================================================
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)