import re
from datetime import datetime

def Remover_Caracteres_Invalidos(texto):
    """Remove caracteres não permitidos no Excel."""
    if isinstance(texto, str):
        return re.sub(r"[\x00-\x1F\x7F]", "", texto)
    return texto

def Formatar_Data(data_str):
    """Formata a data para o formato yyyy-mm-dd."""
    if data_str and isinstance(data_str, str):
        try:
            # Se a data estiver no formato ISO 8601 (como "2025-02-25T14:00:00Z")
            return datetime.fromisoformat(data_str.replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            return "N/A"
    return "N/A"