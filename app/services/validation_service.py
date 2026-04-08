from typing import List, Dict, Any
import pandas as pd
from app.domain.validators import validate_cuit, validate_email
from app.domain.rules import get_required_fields


# =========================================================
# 📌 Servicio de validación de DataFrame (robusto)
# =========================================================
# Mejora clave:
# - Manejo de NaN (pandas)
# - Normalización de datos
# - Evita errores por tipos incorrectos (float, None, etc.)
# - Más seguro para datos reales (inputs sucios)
# =========================================================
def validate_dataframe(
    df: pd.DataFrame,
    process: str,
    client_id: str
) -> List[Dict[str, Any]]:

    errors: List[Dict[str, Any]] = []

    # -----------------------------------------------------
    # 📌 Reglas dinámicas por cliente/proceso
    # -----------------------------------------------------
    required_fields = get_required_fields(client_id, process)

    # -----------------------------------------------------
    # 🔁 Iteración por filas
    # -----------------------------------------------------
    for index, row in df.iterrows():

        row_number = index + 2  # Ajuste por header Excel

        # -------------------------------------------------
        # 📌 Validación de campos obligatorios
        # -------------------------------------------------
        for field in required_fields:
            value = row.get(field)

            # Detecta NaN, None o vacío
            if pd.isna(value) or str(value).strip() == "":
                errors.append({
                    "row": row_number,
                    "field": field,
                    "message": "Campo obligatorio faltante"
                })

        # -------------------------------------------------
        # 📌 Normalización de datos
        # -------------------------------------------------
        cuit = row.get("cuit")
        email = row.get("email")

        # Convertimos a string SOLO si no es NaN
        cuit_str = str(cuit).strip() if not pd.isna(cuit) else None
        email_str = str(email).strip() if not pd.isna(email) else None

        # -------------------------------------------------
        # 📌 Validación de CUIT
        # -------------------------------------------------
        if cuit_str and not validate_cuit(cuit_str):
            errors.append({
                "row": row_number,
                "field": "cuit",
                "message": "CUIT inválido"
            })

        # -------------------------------------------------
        # 📌 Validación de email
        # -------------------------------------------------
        if email_str and not validate_email(email_str):
            errors.append({
                "row": row_number,
                "field": "email",
                "message": "Email inválido"
            })

    return errors