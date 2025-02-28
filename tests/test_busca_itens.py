import asyncio
import aiohttp
from unittest.mock import patch
from src.Busca_Itens import buscar_itens
from src.config import HEADERS

async def testar_busca_itens():
    """Testa a busca de itens para um edital específico."""
    edital_exemplo = {
        "id": "123456",
        "orgao_cnpj": "00000000000191",
        "ano": "2024",
        "numero_sequencial": "0001"
    }

    # Mock para a função buscar_itens
    with patch('src.Busca_Itens.buscar_itens') as mock_buscar_itens:
        # Configura o retorno simulado da função buscar_itens
        mock_buscar_itens.return_value = [
            {'numeroItem': 10001, 'descricao': 'Item 1', 'quantidade': 10, 'valor': 100},
            {'numeroItem': 10002, 'descricao': 'Item 2', 'quantidade': 5, 'valor': 50}
        ]
        
        # Chama a função real para garantir que o mock seja usado
        itens = await buscar_itens(edital_exemplo['orgao_cnpj'], edital_exemplo['ano'], edital_exemplo['numero_sequencial'])
        
        print(f"Total de itens encontrados: {len(itens)}")
        
        if itens:
            print("Exemplo de item:", itens[0])

        # Verifica se a função foi chamada corretamente
        mock_buscar_itens.assert_called_once_with(edital_exemplo['orgao_cnpj'], edital_exemplo['ano'], edital_exemplo['numero_sequencial'])

if __name__ == "__main__":
    asyncio.run(testar_busca_itens())
