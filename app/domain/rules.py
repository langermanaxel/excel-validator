from typing import List, Dict

# Reglas configurables por cliente y proceso
# Permite escalar sin modificar lógica principal
RULES: Dict[str, Dict[str, List[str]]] = {
    "default": {
        "iva": ["cuit", "email", "monto"]
    }
}

# Devuelve los campos obligatorios según cliente y proceso
def get_required_fields(client_id: str, process: str) -> List[str]:
    client_rules = RULES.get(client_id, RULES["default"])
    return client_rules.get(process, ["cuit"])