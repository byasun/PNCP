import asyncio
from src.Busca_Editais import buscar_editais

async def testar_busca_editais():
    """Testa a busca de editais."""
    print("Iniciando teste de busca de editais...")
    editais = await buscar_editais()
    
    print(f"Total de editais encontrados: {len(editais)}")
    
    if editais:
        print("Exemplo de edital:", editais[0])
        print(f"Edital possui {len(editais[0].get('itens', []))} itens.")

if __name__ == "__main__":
    asyncio.run(testar_busca_editais())
