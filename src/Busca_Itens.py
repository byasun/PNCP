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

        if not isinstance(itens, list):  
            print(f"Erro: resposta inesperada da API. Esperado uma lista, mas recebeu {type(itens)}")
            return []

        if not itens:  # Se a lista estiver vazia, não há mais itens para buscar
            break  

        for item in itens:
            item_formatado = {
                "descricao": Remover_Caracteres_Invalidos(item.get("descricao", "")),
                "data": Formatar_Data(item.get("dataInclusao", "")),  # Corrigi para "dataInclusao"
                "quantidade": item.get("quantidade", 0),
                "valor": item.get("valorUnitarioEstimado", 0),  # Ajustei para "valorUnitarioEstimado"
            }
            todos_itens.append(item_formatado)
        
        pagina += 1

    return todos_itens