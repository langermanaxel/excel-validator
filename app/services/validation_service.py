from typing import List, Dict, Any
import pandas as pd
from app.domain.validators import validate_cuit, validate_email
from app.domain.rules import get_required_fields


# =========================================================
# 📌 Servicio de validación de DataFrame
# =========================================================
# Esta función es el núcleo del sistema de validación.
# Se encarga de aplicar reglas dinámicas y validaciones
# de negocio sobre los datos cargados desde un archivo.
#
# Decisiones de diseño:
# - Se separa en la capa de servicios (no en la API)
# - Cumple con el principio de responsabilidad única (SRP)
# - Desacopla reglas (rules.py) y validaciones (validators.py)
#
# Parámetros:
# - df: DataFrame con los datos a validar
# - process: tipo de proceso (ej: iva, facturación)
# - client_id: identificador del cliente (multi-tenant)
#
# Retorna:
# - Lista de errores encontrados (estructura uniforme)
# =========================================================
def validate_dataframe(
    df: pd.DataFrame,
    process: str,
    client_id: str
) -> List[Dict[str, Any]]:

    # Lista donde se acumulan los errores encontrados
    errors: List[Dict[str, Any]] = []

    # -----------------------------------------------------
    # 📌 Obtención de reglas dinámicas
    # -----------------------------------------------------
    # Se obtienen los campos obligatorios según cliente y proceso
    # Esto permite que el sistema sea configurable y escalable
    required_fields = get_required_fields(client_id, process)

    # -----------------------------------------------------
    # 🔁 Iteración por filas del DataFrame
    # -----------------------------------------------------
    for index, row in df.iterrows():

        # Ajustamos el número de fila para que coincida con Excel
        # (index empieza en 0, Excel en 1 + header)
        row_number = index + 2

        # -------------------------------------------------
        # 📌 Validación de campos obligatorios
        # -------------------------------------------------
        for field in required_fields:

            # pd.isna detecta valores nulos, vacíos o NaN
            if pd.isna(row.get(field)):
                errors.append({
                    "row": row_number,
                    "field": field,
                    "message": "Campo obligatorio faltante"
                })

        # -------------------------------------------------
        # 📌 Validaciones de negocio específicas
        # -------------------------------------------------

        # Validación de CUIT
        # Se convierte a string para evitar problemas de tipo (ej: float)
        if "cuit" in row and not validate_cuit(str(row.get("cuit"))):
            errors.append({
                "row": row_number,
                "field": "cuit",
                "message": "CUIT inválido"
            })

        # Validación de email
        if "email" in row and not validate_email(row.get("email")):
            errors.append({
                "row": row_number,
                "field": "email",
                "message": "Email inválido"
            })

    # Retornamos todos los errores encontrados
    return errors