import pandas as pd
from fastapi import UploadFile

# Encapsulamos la lectura de archivos para no mezclar lógica en la API
def read_file(file: UploadFile) -> pd.DataFrame:
    filename = file.filename.lower()

    # Soporte CSV
    if filename.endswith(".csv"):
        return pd.read_csv(file.file)

    # Soporte Excel
    if filename.endswith(".xlsx"):
        return pd.read_excel(file.file)

    # Validación de formato
    raise ValueError("Formato de archivo no soportado")