import asyncio
import aiohttp
import requests
import pandas as pd
import re
from datetime import datetime, timedelta

# URL base da API
BASE_URL = "https://pncp.gov.br/api/search/"

# Cabeçalhos da requisição
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://pncp.gov.br",
    "Origin": "https://pncp.gov.br"
}

def remover_caracteres_invalidos(texto):
    """Remove caracteres não permitidos no Excel."""
    if isinstance(texto, str):
        return re.sub(r"[\x00-\x1F\x7F]", "", texto)  # Remove caracteres de controle ASCII
    return texto

def calcular_data_limite():
    """Calcula a data limite (D-15) em relação à data atual."""
    hoje = datetime.now()
    data_limite = hoje - timedelta(days=15)
    return data_limite.strftime("%Y-%m-%d")

def formatar_data(data):
    """Formata a data para exibir apenas yyyy-mm-dd, removendo informações adicionais."""
    return data.split("T")[0] if data and "T" in data else "N/A"

async def buscar_itens_em_lote(editais, semaforo):
    """Busca os itens de vários editais em paralelo usando a URL correta."""
    itens_lista = []

    async def fetch(session, edital):
        try:
            cnpj = edital.get("orgao_cnpj", "").strip()
            ano = edital.get("ano", "").strip()
            num_seq = edital.get("numero_sequencial", "").strip()

            if not cnpj or not ano or not num_seq:
                return

            url = f"https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{num_seq}/itens"

            async with semaforo, session.get(url, headers=HEADERS) as resposta:
                if resposta.status == 200:
                    dados = await resposta.json()

                    if isinstance(dados, list):
                        for item in dados:
                            item_info = {
                                "ID Edital": edital.get("id", "N/A"),
                                "Número Item": item.get("numeroItem", "N/A"),
                                "Descrição Item": remover_caracteres_invalidos(item.get("descricao", "N/A")),
                                "Material ou Serviço": item.get("materialOuServicoNome", "N/A"),
                                "Valor Unitário Estimado": item.get("valorUnitarioEstimado", "N/A"),
                                "Valor Total": item.get("valorTotal", "N/A"),
                                "Quantidade": item.get("quantidade", "N/A"),
                                "Unidade Medida": item.get("unidadeMedida", "N/A"),
                                "Critério de Julgamento": item.get("criterioJulgamentoNome", "N/A"),
                                "Situação do Item": item.get("situacaoCompraItemNome", "N/A"),
                                "Tipo de Benefício": item.get("tipoBeneficioNome", "N/A"),
                                "Data Inclusão": formatar_data(item.get("dataInclusao", "N/A")),
                                "Data Atualização": formatar_data(item.get("dataAtualizacao", "N/A"))
                            }
                            itens_lista.append(item_info)
        except Exception as e:
            print(f"Erro ao buscar itens para {edital.get('id', 'N/A')}: {str(e)}")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, edital) for edital in editais]
        await asyncio.gather(*tasks)

    return itens_lista

def buscar_editais():
    """Busca todos os editais disponíveis na API do PNCP."""
    todos_editais = []
    pagina = 1
    tam_pagina = 100
    data_limite = calcular_data_limite()

    try:
        while True:
            params = {
                "tipos_documento": "edital",
                "ordenacao": "-data",
                "pagina": pagina,
                "tam_pagina": tam_pagina,
                "status": "recebendo_proposta",
                "dataDivulgacaoPNCP__lte": data_limite
            }

            print(f"Consultando página {pagina}...")
            resposta = requests.get(BASE_URL, headers=HEADERS, params=params)

            if resposta.status_code == 200:
                dados_json = resposta.json()
                dados = dados_json.get("items", [])

                if not dados:
                    print("Nenhum edital encontrado.")
                    break  

                for edital in dados:
                    edital_info = {chave: remover_caracteres_invalidos(edital.get(chave, "N/A")) for chave in edital}
                    todos_editais.append(edital_info)

                print(f"Editais encontrados na página {pagina}: {len(dados)}")
                pagina += 1 
                
                if pagina * tam_pagina > 10000:
                    print("⚠️ Alcançado o limite de 10.000 resultados. Considere filtrar melhor a busca.")
                    break
                
            else:
                print(f"Erro ao buscar editais: {resposta.status_code} - {resposta.text}")
                break

    except Exception as e:
        print(f"Erro ao buscar editais: {str(e)}")

    # Buscar os itens em lote para todos os editais
    if todos_editais:
        try:
            print("Buscando itens de todos os editais em paralelo...")
            semaforo = asyncio.Semaphore(10)  
            itens_lista = asyncio.run(buscar_itens_em_lote(todos_editais, semaforo))  
        except Exception as e:
            print(f"Erro ao buscar os itens: {str(e)}")
            itens_lista = []

    print(f"Total de editais encontrados: {len(todos_editais)}")
    return todos_editais, itens_lista

def salvar_em_excel(editais, itens, nome_arquivo="editais.xlsx"):
    """Salva os editais e itens em um arquivo Excel com duas abas."""
    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        df_editais = pd.DataFrame(editais)
        df_itens = pd.DataFrame(itens)

        df_editais.to_excel(writer, sheet_name="Editais", index=False)
        df_itens.to_excel(writer, sheet_name="Itens", index=False)

    print(f"Arquivo salvo com sucesso: {nome_arquivo}")

# Executa a busca e salva no Excel
editais, itens = buscar_editais()
salvar_em_excel(editais, itens)
