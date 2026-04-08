import re
from typing import Optional

# Validación de CUIT basada en algoritmo oficial
# Separamos esta lógica porque es parte del dominio (reglas de negocio)
def validate_cuit(cuit: Optional[str]) -> bool:
    if not cuit:
        return False

    # Eliminamos cualquier carácter no numérico
    digits = re.sub(r"\D", "", cuit)

    if len(digits) != 11:
        return False

    # Factores definidos por AFIP
    factors = [5,4,3,2,7,6,5,4,3,2]

    # Calculamos checksum
    total = sum(int(digits[i]) * factors[i] for i in range(10))
    remainder = total % 11
    check_digit = 11 - remainder

    # Ajustes según reglas
    if check_digit == 11:
        check_digit = 0
    elif check_digit == 10:
        check_digit = 9

    return check_digit == int(digits[-1])


# Validación simple de email usando regex
def validate_email(email: Optional[str]) -> bool:
    if not email:
        return False

    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email) is not None