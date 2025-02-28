import random
from src.config import BASE_URL_ITENS, HEADERS
from src.API.api_client import ApiClient
from src.utils import Remover_Caracteres_Invalidos, Formatar_Data

async def buscar_itens(cnpj, ano, num_seq):
    """Busca os itens de um edital específico usando ApiClient."""
    client = ApiClient(BASE_URL_ITENS, HEADERS)
    
    pagina = 1
    tam_pagina = 50
    todos_itens = []

    while True:
        itens = await client.get_itens(cnpj, ano, num_seq, pagina=pagina, tam_pagina=tam_pagina)
        if itens:
            items = itens.get("items", [])
            if not items:
                break

            for item in items:
                # Processamento dos itens
                item_formatado = {
                    "descricao": Remover_Caracteres_Invalidos(item.get("descricao", "")),
                    "data": Formatar_Data(item.get("data", "")),
                    "quantidade": item.get("quantidade", ""),
                    "valor": item.get("valor", ""),
                }
                todos_itens.append(item_formatado)
            
            pagina += 1
        else:
            print(f"Erro ao buscar itens do edital {num_seq}.")
            break

    return todos_itens
