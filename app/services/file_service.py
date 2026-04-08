import pandas as pd
from fastapi import UploadFile


# =========================================================
# 📌 Servicio de lectura de archivos
# =========================================================
# Esta función encapsula la lógica de lectura de archivos
# para evitar mezclarla con la capa de API.
#
# Decisión de diseño:
# - Se separa en un servicio para mantener la API limpia
# - Permite reutilizar la lógica en otros contextos
# - Facilita testing independiente
#
# Soporta:
# - CSV
# - Excel (.xlsx)
#
# Parámetro:
# - file: UploadFile (archivo subido vía FastAPI)
#
# Retorna:
# - DataFrame de pandas con los datos del archivo
#
# Lanza:
# - ValueError si el formato no es soportado
# =========================================================
def read_file(file: UploadFile) -> pd.DataFrame:

    # Normalizamos el nombre del archivo para evitar problemas
    # con mayúsculas/minúsculas (ej: .CSV, .XLSX)
    filename = file.filename.lower()

    # -----------------------------------------------------
    # 📄 Lectura de archivos CSV
    # -----------------------------------------------------
    # Se utiliza pandas.read_csv para convertir el archivo
    # en un DataFrame (estructura tabular)
    if filename.endswith(".csv"):
        return pd.read_csv(file.file, dtype=str)

    # -----------------------------------------------------
    # 📊 Lectura de archivos Excel
    # -----------------------------------------------------
    # Se utiliza pandas.read_excel para archivos .xlsx
    if filename.endswith(".xlsx"):
        return pd.read_excel(file.file, dtype=str)

    # -----------------------------------------------------
    # ❌ Validación de formato
    # -----------------------------------------------------
    # Si el archivo no es CSV ni Excel, se lanza un error
    # controlado que será manejado en la capa de API
    raise ValueError("Formato de archivo no soportado")