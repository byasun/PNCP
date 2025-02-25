import aiohttp
import asyncio
from src.config import BASE_URL, HEADERS
from src.utils import Formatar_Data, Remover_Caracteres_Invalidos

async def buscar_editais():
    """Busca todos os editais disponíveis na API do PNCP de forma assíncrona."""
    todos_editais = []
    pagina = 1
    tam_pagina = 100

    async with aiohttp.ClientSession() as session:
        while True:
            params = {
                "tipos_documento": "edital",
                "ordenacao": "-data",
                "pagina": pagina,
                "tam_pagina": tam_pagina,
                "status": "recebendo_proposta"
            }

            print(f"Buscando editais - Página {pagina}...")
            async with session.get(BASE_URL, headers=HEADERS, params=params) as resposta:
                if resposta.status == 200:
                    dados = await resposta.json()
                    items = dados.get("items", [])
                    if not items:
                        break

                    for edital in items:
                        edital_info = {chave: Remover_Caracteres_Invalidos(edital.get(chave, "N/A")) for chave in edital}
                        edital_info["data_publicacao_pncp"] = Formatar_Data(edital_info.get("data_publicacao_pncp"))
                        todos_editais.append(edital_info)

                    pagina += 1
                else:
                    print(f"Erro ao buscar editais: {resposta.status} - {resposta.text}")
                    break
    return todos_editais

async def buscar_editais_em_lote():
    """Função principal para executar as buscas."""
    return await buscar_editais()
