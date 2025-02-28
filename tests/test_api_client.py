import asyncio
from src.API.api_client import ApiClient
from src.config import BASE_URL, HEADERS

async def testar_get_editais():
    """Testa a busca de editais via ApiClient."""
    print("Iniciando teste da API Client para editais...")

    client = ApiClient(BASE_URL, HEADERS)
    resposta = await client.get_editais()

    if isinstance(resposta, dict) and "items" in resposta:
        editais = resposta["items"]  # 🔹 Agora pegamos apenas a lista de editais
    else:
        print("Erro: A resposta da API não contém 'items'.")
        return

    print(f"Total de editais encontrados: {len(editais)}")

    if editais:
        print("Exemplo de edital:", editais[0])  # Exibe um exemplo de edital

if __name__ == "__main__":
    asyncio.run(testar_get_editais())
