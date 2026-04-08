from typing import List, Dict, Any
import pandas as pd
from app.domain.validators import validate_cuit, validate_email
from app.domain.rules import get_required_fields

# Servicio principal de validación
# Se mantiene separado para cumplir SRP (Single Responsibility Principle)
def validate_dataframe(
    df: pd.DataFrame,
    process: str,
    client_id: str
) -> List[Dict[str, Any]]:

    errors: List[Dict[str, Any]] = []

    # Obtenemos reglas dinámicas
    required_fields = get_required_fields(client_id, process)

    for index, row in df.iterrows():
        row_number = index + 2  # Ajuste por header

        # Validación de campos obligatorios
        for field in required_fields:
            if pd.isna(row.get(field)):
                errors.append({
                    "row": row_number,
                    "field": field,
                    "message": "Campo obligatorio faltante"
                })

        # Validaciones de negocio
        if "cuit" in row and not validate_cuit(str(row.get("cuit"))):
            errors.append({
                "row": row_number,
                "field": "cuit",
                "message": "CUIT inválido"
            })

        if "email" in row and not validate_email(row.get("email")):
            errors.append({
                "row": row_number,
                "field": "email",
                "message": "Email inválido"
            })

    return errors