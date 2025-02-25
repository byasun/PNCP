import aiohttp
import asyncio
from src.config import BASE_URL, HEADERS
from src.utils import Formatar_Data, Remover_Caracteres_Invalidos

async def buscar_atas():
    """Busca todas as atas vigentes na API do PNCP de forma assíncrona."""
    todas_atas = []
    pagina = 1
    tam_pagina = 100

    async with aiohttp.ClientSession() as session:
        while True:
            params = {
                "tipos_documento": "ata",
                "ordenacao": "-data",
                "pagina": pagina,
                "tam_pagina": tam_pagina,
                "status": "vigente"
            }

            print(f"Buscando atas vigentes - Página {pagina}...")
            async with session.get(BASE_URL, headers=HEADERS, params=params) as resposta:
                if resposta.status == 200:
                    dados = await resposta.json()
                    items = dados.get("items", [])
                    if not items:
                        break

                    for ata in items:
                        ata_info = {chave: Remover_Caracteres_Invalidos(ata.get(chave, "N/A")) for chave in ata}
                        ata_info["data_publicacao_pncp"] = Formatar_Data(ata_info.get("data_publicacao_pncp"))
                        todas_atas.append(ata_info)

                    pagina += 1
                else:
                    print(f"Erro ao buscar atas: {resposta.status} - {resposta.text}")
                    break
    return todas_atas

async def buscar_atas_em_lote():
    """Função principal para executar as buscas."""
    return await buscar_atas()
