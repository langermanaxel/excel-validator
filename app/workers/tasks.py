from app.core.celery_app import celery_app
from app.services.validation_service import validate_dataframe
from app.services.report_service import generate_error_report
from typing import List, Dict


# =========================================================
# 📌 Tarea asíncrona de validación de archivos
# =========================================================
# Esta función es ejecutada por un worker de Celery.
# Se encarga de procesar los datos en segundo plano,
# evitando bloquear la API principal.
#
# Decisiones de diseño:
# - Se usa Celery para desacoplar procesamiento pesado
# - La tarea recibe datos serializables (List[Dict])
# - Se delega la lógica a servicios para mantener SRP
#
# Parámetros:
# - data: lista de registros (proveniente del DataFrame)
# - process: tipo de proceso (ej: iva)
# - client_id: identificador del cliente (multi-tenant)
#
# Retorna:
# - Diccionario con estado, cantidad de errores y reporte
# =========================================================
@celery_app.task
def validate_file_task(
    data: List[Dict],
    process: str,
    client_id: str
):
    import pandas as pd

    # -----------------------------------------------------
    # 📌 Reconstrucción del DataFrame
    # -----------------------------------------------------
    # Convertimos la lista de diccionarios nuevamente a DataFrame
    # para poder reutilizar la lógica basada en pandas
    df = pd.DataFrame(data)

    # -----------------------------------------------------
    # 📌 Validación de datos
    # -----------------------------------------------------
    # Delegamos la lógica al servicio de validación
    # (separación de responsabilidades)
    errors = validate_dataframe(df, process, client_id)

    # -----------------------------------------------------
    # 📌 Generación de reporte
    # -----------------------------------------------------
    # Solo generamos archivo si existen errores
    report = None
    if errors:
        report = generate_error_report(errors)

    # -----------------------------------------------------
    # 📌 Respuesta de la tarea
    # -----------------------------------------------------
    # Se devuelve un resumen del resultado:
    # - status: ok o error
    # - total_errors: cantidad de errores encontrados
    # - report: archivo generado (si aplica)
    return {
        "status": "error" if errors else "ok",
        "total_errors": len(errors),
        "report": report
    }