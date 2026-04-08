import pandas as pd
import uuid
from typing import List, Dict

# Genera un archivo con los errores encontrados
# Se separa para reutilización y claridad
def generate_error_report(errors: List[Dict]) -> str:
    filename = f"report_{uuid.uuid4().hex}.csv"

    df = pd.DataFrame(errors)
    df.to_csv(filename, index=False)

    return filename