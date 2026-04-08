from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from app.services.file_service import read_file
from app.workers.tasks import validate_file_task
from app.core.celery_app import celery_app

# Router de FastAPI que agrupa endpoints relacionados
router = APIRouter()


# =========================================================
# 📌 Endpoint: Validación de archivo
# =========================================================
# Este endpoint recibe un archivo (CSV o Excel) y dispara
# su procesamiento de manera asíncrona utilizando Celery.
#
# Decisión de diseño:
# - Se utiliza procesamiento async para evitar bloquear la API
# - La validación pesada se delega a un worker
# - Se devuelve un task_id para consultar el estado posteriormente
# =========================================================
@router.post("/validate-file")
async def validate_file(
    # UploadFile permite manejar archivos grandes sin cargarlos
    # completamente en memoria (más eficiente que bytes)
    file: UploadFile = File(...),

    # Tipo de proceso a validar (ej: iva, facturación, etc.)
    # Se define un valor por defecto para simplificar el uso
    process: str = Query("iva"),

    # Identificador del cliente (permite lógica multi-tenant)
    client_id: str = Query("default")
):
    try:
        # La lectura del archivo se delega a un servicio
        # para mantener separación de responsabilidades
        df = read_file(file)

    except ValueError as e:
        # Si el archivo tiene formato inválido (ej: extensión no soportada),
        # devolvemos un error controlado al cliente (HTTP 400)
        raise HTTPException(status_code=400, detail=str(e))

    # Convertimos el DataFrame a lista de diccionarios
    # para poder serializarlo y enviarlo a Celery
    data = df.to_dict(orient="records")

    # Enviamos la tarea a la cola (no bloquea la request)
    # Celery la ejecutará en segundo plano
    task = validate_file_task.delay(data, process, client_id)

    # Devolvemos el ID de la tarea para seguimiento
    return {"task_id": task.id}


# =========================================================
# 📌 Endpoint: Estado de la tarea
# =========================================================
# Permite consultar el estado de una tarea previamente enviada.
#
# Estados posibles:
# - PENDING: aún no procesada
# - SUCCESS: finalizada correctamente
# - FAILURE: error durante ejecución
#
# Decisión de diseño:
# - Se utiliza celery_app.AsyncResult para asegurar que se use
#   el backend configurado (Redis) y evitar inconsistencias
# =========================================================
@router.get("/task-status/{task_id}")
def get_status(task_id: str):

    # Recuperamos el estado de la tarea desde el backend (Redis)
    task = celery_app.AsyncResult(task_id)

    # La tarea aún no fue procesada
    if task.state == "PENDING":
        return {"status": "pending"}

    # La tarea finalizó correctamente
    # Se devuelve directamente el resultado generado por el worker
    if task.state == "SUCCESS":
        return task.result

    # Otros estados posibles (ej: FAILURE, RETRY, etc.)
    # Se devuelve el estado para diagnóstico
    return {"status": task.state}