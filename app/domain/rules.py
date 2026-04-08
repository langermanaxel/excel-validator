from typing import List, Dict


# =========================================================
# 📌 Definición de reglas de validación
# =========================================================
# RULES define qué campos son obligatorios según:
# - cliente (client_id)
# - proceso (process)
#
# Estructura:
# {
#   "cliente": {
#       "proceso": [campos obligatorios]
#   }
# }
#
# Ejemplo:
# - Para el cliente "default" y proceso "iva",
#   se requieren los campos: cuit, email, monto
#
# Decisión de diseño:
# - Permite configurar reglas sin modificar lógica de validación
# - Facilita soporte multi-tenant (múltiples clientes)
# - Hace el sistema extensible y mantenible
# =========================================================
RULES: Dict[str, Dict[str, List[str]]] = {
    "default": {
        "iva": ["cuit", "email", "monto"]
    }
}


# =========================================================
# 📌 Función: obtener campos obligatorios
# =========================================================
# Devuelve la lista de campos requeridos según:
# - client_id: identifica al cliente
# - process: tipo de proceso (ej: iva, facturación, etc.)
#
# Lógica:
# 1. Busca reglas específicas del cliente
# 2. Si no existen, usa reglas "default"
# 3. Si el proceso no está definido, usa ["cuit"] como fallback
#
# Beneficio:
# - Evita errores por configuraciones faltantes
# - Hace el sistema más robusto y tolerante
# =========================================================
def get_required_fields(client_id: str, process: str) -> List[str]:

    # Obtiene reglas del cliente o usa las por defecto
    client_rules = RULES.get(client_id, RULES["default"])

    # Devuelve los campos requeridos para el proceso
    # Si no existe, usa un fallback mínimo
    return client_rules.get(process, ["cuit"])