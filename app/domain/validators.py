import re
from typing import Optional


# =========================================================
# 📌 Validación de CUIT
# =========================================================
# Esta función valida un CUIT argentino utilizando
# el algoritmo oficial basado en un dígito verificador.
#
# Decisión de diseño:
# - Se ubica en la capa de dominio porque representa
#   una regla de negocio específica
# - Se separa de la API y servicios para reutilización
#   y testeo independiente
#
# Parámetro:
# - cuit: string opcional que representa el CUIT
#
# Retorna:
# - True si el CUIT es válido
# - False en caso contrario
# =========================================================
def validate_cuit(cuit: Optional[str]) -> bool:

    # Validación básica: valor nulo o vacío
    if not cuit:
        return False

    # Eliminamos cualquier carácter no numérico
    # (permite inputs como "20-12345678-9")
    digits = re.sub(r"\D", "", cuit)

    # El CUIT debe tener exactamente 11 dígitos
    if len(digits) != 11:
        return False

    # Factores definidos por AFIP para cálculo del dígito verificador
    factors = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    # Calculamos la suma ponderada de los primeros 10 dígitos
    total = sum(int(digits[i]) * factors[i] for i in range(10))

    # Obtenemos el resto de la división por 11
    remainder = total % 11

    # Calculamos el dígito verificador esperado
    check_digit = 11 - remainder

    # Ajustes según reglas del algoritmo
    if check_digit == 11:
        check_digit = 0
    elif check_digit == 10:
        check_digit = 9

    # Comparamos con el último dígito del CUIT
    return check_digit == int(digits[-1])


# =========================================================
# 📌 Validación de email
# =========================================================
# Validación básica de formato de email utilizando regex.
#
# Nota:
# - No valida existencia real del email
# - Solo valida estructura (usuario@dominio.ext)
#
# Decisión de diseño:
# - Validación liviana para evitar inputs incorrectos
# - Se puede extender con validaciones más estrictas
# =========================================================
def validate_email(email: Optional[str]) -> bool:

    # Validación básica: valor nulo o vacío
    if not email:
        return False

    # Expresión regular simple para validar formato de email
    pattern = r"[^@]+@[^@]+\.[^@]+"

    # re.match valida desde el inicio del string
    return re.match(pattern, email) is not None