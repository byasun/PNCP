import asyncio
from src.config import BASE_URL, HEADERS
from src.API.api_client import ApiClient
from src.Busca_Itens import buscar_itens
from src.utils import Remover_Caracteres_Invalidos, Formatar_Data

async def buscar_editais():
    """Busca todos os editais da API e retorna sem alterações."""
    todos_editais = []
    pagina = 1
    tam_pagina = 100
    client = ApiClient(BASE_URL, HEADERS)

    while True:
        editais = await client.get_editais(pagina=pagina, tam_pagina=tam_pagina)
        
        if not editais or "items" not in editais:
            print("Erro ao buscar editais ou resposta inválida.")
            break

        items = editais["items"]
        if not items:
            break

        todos_editais.extend(items)  # Adiciona os editais sem modificar nada

        print(f"Página {pagina}: {len(items)} editais coletados.")  # Mensagem de progresso das páginas de editais

        pagina += 1

    return todos_editais

async def buscar_itens_para_todos_editais(editais):
    """Busca os itens para todos os editais coletados."""
    todos_itens = []
    
    for edital in editais:
        cnpj = edital.get("orgao_cnpj", "")
        ano = edital.get("ano", "")
        num_seq = edital.get("numero_sequencial", "")

        if cnpj and ano and num_seq:
            itens = await buscar_itens(cnpj, ano, num_seq)
            for item in itens:
                item["edital_id"] = num_seq  # Relaciona o item ao edital correto
            todos_itens.extend(itens)

            # Removido qualquer tipo de print do JSON de retorno da API aqui
            # Não há mais nenhuma impressão do conteúdo de "itens" ou dados retornados pela API.

    return todos_itens
