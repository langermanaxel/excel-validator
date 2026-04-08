from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from app.services.file_service import read_file
from app.workers.tasks import validate_file_task
from app.core.celery_app import celery_app

router = APIRouter()

# Endpoint principal: recibe archivo y lo envía a procesar async
@router.post("/validate-file")
async def validate_file(
    file: UploadFile = File(...),
    process: str = Query("iva"),
    client_id: str = Query("default")
):
    try:
        # Lectura desacoplada
        df = read_file(file)
    except ValueError as e:
        # Manejo correcto de errores para el cliente
        raise HTTPException(status_code=400, detail=str(e))

    data = df.to_dict(orient="records")

    # Enviamos tarea a la cola (no bloquea)
    task = validate_file_task.delay(data, process, client_id)

    return {"task_id": task.id}


# Endpoint para consultar estado del procesamiento
@router.get("/task-status/{task_id}")
def get_status(task_id: str):
    task = celery_app.AsyncResult(task_id)

    if task.state == "PENDING":
        return {"status": "pending"}

    if task.state == "SUCCESS":
        return task.result

    return {"status": task.state}