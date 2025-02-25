import aiohttp
import asyncio
from src.config import BASE_URL, HEADERS
from src.utils import Formatar_Data, Remover_Caracteres_Invalidos

async def buscar_contratos():
    """Busca todos os contratos vigentes na API do PNCP de forma assíncrona."""
    todos_contratos = []
    pagina = 1
    tam_pagina = 100

    async with aiohttp.ClientSession() as session:
        while True:
            params = {
                "tipos_documento": "contrato",
                "ordenacao": "-data",
                "pagina": pagina,
                "tam_pagina": tam_pagina,
                "status": "vigente"
            }

            print(f"Buscando contratos vigentes - Página {pagina}...")
            async with session.get(BASE_URL, headers=HEADERS, params=params) as resposta:
                if resposta.status == 200:
                    dados = await resposta.json()
                    items = dados.get("items", [])
                    if not items:
                        break

                    for contrato in items:
                        contrato_info = {chave: Remover_Caracteres_Invalidos(contrato.get(chave, "N/A")) for chave in contrato}
                        contrato_info["data_publicacao_pncp"] = Formatar_Data(contrato_info.get("data_publicacao_pncp"))
                        todos_contratos.append(contrato_info)

                    pagina += 1
                else:
                    print(f"Erro ao buscar contratos: {resposta.status} - {resposta.text}")
                    break
    return todos_contratos

async def buscar_contratos_em_lote():
    """Função principal para executar as buscas."""
    return await buscar_contratos()
