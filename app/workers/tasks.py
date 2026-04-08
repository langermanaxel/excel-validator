from app.core.celery_app import celery_app
from app.services.validation_service import validate_dataframe
from app.services.report_service import generate_error_report
from typing import List, Dict

# Tarea asíncrona ejecutada por el worker
# Permite procesar archivos sin bloquear la API
@celery_app.task
def validate_file_task(
    data: List[Dict],
    process: str,
    client_id: str
):
    import pandas as pd

    df = pd.DataFrame(data)

    # Delegamos la lógica al servicio correspondiente
    errors = validate_dataframe(df, process, client_id)

    report = None
    if errors:
        report = generate_error_report(errors)

    return {
        "status": "error" if errors else "ok",
        "total_errors": len(errors),
        "report": report
    }