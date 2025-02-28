import asyncio
import aiohttp
from src.Busca_Itens import buscar_itens_de_edital
from src.config import HEADERS

async def testar_busca_itens():
    """Testa a busca de itens para um edital específico."""
    edital_exemplo = {
        "id": "123456",
        "orgao_cnpj": "00000000000191",
        "ano": "2024",
        "numero_sequencial": "0001"
    }

    async with aiohttp.ClientSession() as session:
        semaforo = asyncio.Semaphore(10)
        itens = await buscar_itens_de_edital(session, edital_exemplo, semaforo)
    
    print(f"Total de itens encontrados: {len(itens)}")
    
    if itens:
        print("Exemplo de item:", itens[0])

if __name__ == "__main__":
    asyncio.run(testar_busca_itens())
