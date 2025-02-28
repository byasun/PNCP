import re
from datetime import datetime

def Remover_Caracteres_Invalidos(texto):
    """Remove caracteres não permitidos no Excel."""
    if isinstance(texto, str):
        return re.sub(r"[\x00-\x1F\x7F]", "", texto)
    return texto

def Formatar_Data(data_str):
    """Formata a data para o formato yyyy-MM-dd, tratando diferentes formatos de entrada."""
    if not data_str or not isinstance(data_str, str):
        return "N/A"

    try:
        if "T" in data_str:  # Formato ISO 8601 (ex: "2025-02-25T14:00:00Z")
            return datetime.fromisoformat(data_str.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        return datetime.strptime(data_str[:10], "%Y-%m-%d").strftime("%Y-%m-%d")  # Corta qualquer hora extra
    except ValueError:
        return "N/A"
