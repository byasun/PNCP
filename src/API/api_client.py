import aiohttp
import asyncio
import time
from src.config import BASE_URL, BASE_URL_ITENS, HEADERS

class ApiClient:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    async def get_data(self, params, url_extension=""):
        """Função genérica para buscar dados da API."""
        url = f"{self.base_url}/{url_extension}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as resposta:
                    if resposta.status == 200:
                        return await resposta.json()
                    elif resposta.status == 429:
                        print("Limite de requisições alcançado, esperando...")
                        await asyncio.sleep(10)
                        return await self.get_data(params, url_extension)
                    else:
                        print(f"Erro {resposta.status} ao acessar a API.")
                        return None
            except Exception as e:
                print(f"Erro ao fazer requisição para {url}: {str(e)}")
                return None

    async def get_editais(self, pagina=1, tam_pagina=100):
        """Busca editais."""
        params = {
            "tipos_documento": "edital",
            "ordenacao": "-data",
            "pagina": pagina,
            "tam_pagina": tam_pagina,
            "status": "recebendo_proposta"
        }
        return await self.get_data(params)

    async def get_itens(self, cnpj, ano, num_seq, pagina=1, tam_pagina=50):
        """Busca os itens de um edital específico."""
        url_extension = f"{cnpj}/compras/{ano}/{num_seq}/itens"
        params = {"pagina": pagina, "tamanhoPagina": tam_pagina}
        return await self.get_data(params, url_extension)
