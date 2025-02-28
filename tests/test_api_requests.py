import requests
from src.config import BASE_URL, HEADERS

def testar_api_editais():
    """Testa se a API está retornando os editais corretamente."""
    params = {
        "tipos_documento": "edital",
        "ordenacao": "-data",
        "pagina": 1,
        "tam_pagina": 10,
        "status": "recebendo_proposta"
    }

    print("Testando a API de editais...")
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("Exemplo de resposta:", data)
    else:
        print("Erro ao acessar a API:", response.text)

if __name__ == "__main__":
    testar_api_editais()
