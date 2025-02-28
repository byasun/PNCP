import asyncio
from src.config import BASE_URL, HEADERS
from src.API.api_client import ApiClient
from src.Busca_Itens import buscar_itens
from src.utils import Remover_Caracteres_Invalidos, Formatar_Data

async def buscar_editais():
    """Busca os editais e chama a função de itens para cada edital."""
    todos_editais = []
    pagina = 1
    tam_pagina = 100
    client = ApiClient(BASE_URL, HEADERS)

    while True:
        editais = await client.get_editais(pagina=pagina, tam_pagina=tam_pagina)
        if editais:
            items = editais.get("items", [])
            if not items:
                break

            for edital in items:
                # Processamento dos editais
                edital_formatado = {
                    "numero": edital.get("numero_sequencial", ""),
                    "orgao": Remover_Caracteres_Invalidos(edital.get("orgao", "")),
                    "data": Formatar_Data(edital.get("data_publicacao", "")),
                    # Outros campos que você queira formatar
                }
                todos_editais.append(edital_formatado)

                # Agora, busca os itens do edital
                cnpj = edital.get("cnpj")
                ano = edital.get("ano")
                num_seq = edital.get("numero_sequencial")
                itens = await buscar_itens(cnpj, ano, num_seq)
                
                # Se você precisar fazer algo com os itens retornados, pode processar aqui
                print(f"Itens do edital {num_seq}: {itens}")

            pagina += 1
        else:
            print("Erro ao buscar editais ou resposta inválida.")
            break

    return todos_editais
