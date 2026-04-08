import pandas as pd
import uuid
from typing import List, Dict


# =========================================================
# 📌 Generación de reporte de errores
# =========================================================
# Esta función se encarga de generar un archivo CSV con los
# errores encontrados durante el proceso de validación.
#
# Decisión de diseño:
# - Se separa de la lógica de validación para mantener
#   responsabilidades claras (Single Responsibility)
# - Permite reutilizar la generación de reportes en otros procesos
# - Facilita testing independiente
#
# Parámetro:
# - errors: lista de diccionarios, donde cada elemento
#   representa un error (ej: fila, campo, descripción)
#
# Retorna:
# - filename: nombre del archivo generado
#
# Ejemplo de error:
# {
#   "row": 1,
#   "field": "email",
#   "error": "Formato inválido"
# }
# =========================================================
def generate_error_report(errors: List[Dict]) -> str:

    # Generamos un nombre único para evitar colisiones
    # entre múltiples ejecuciones concurrentes
    filename = f"report_{uuid.uuid4().hex}.csv"

    # Convertimos la lista de errores en un DataFrame
    # para facilitar la exportación a CSV
    df = pd.DataFrame(errors)

    # Guardamos el archivo en disco
    # index=False evita agregar una columna extra con índices
    df.to_csv(filename, index=False)

    # Retornamos el nombre del archivo para que pueda ser
    # descargado o referenciado posteriormente
    return filename