import requests
import pandas as pd
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

# Função para calcular a data limite (D-15)
def calcular_data_limite():
    hoje = datetime.now()
    data_limite = hoje - timedelta(days=15)
    return data_limite.strftime("%Y-%m-%d")

def buscar_editais():
    """Busca todos os editais disponíveis na API do PNCP."""
    todos_editais = []
    pagina = 1
    tam_pagina = 100  
    data_limite = calcular_data_limite()  

    while True:
        params = {
            "tipos_documento": "edital",
            "ordenacao": "-data",
            "pagina": pagina,
            "tam_pagina": tam_pagina,
            "status": "recebendo_proposta",
            "data_publicacao_pncp__lte": data_limite  # Filtro correto para data de publicação
        }

        print(f"Consultando página {pagina}...")
        resposta = requests.get(BASE_URL, headers=HEADERS, params=params)

        if resposta.status_code == 200:
            dados_json = resposta.json()

            dados = dados_json.get("items", [])

            if not dados:
                print("Nenhum edital encontrado.")
                break  

            # Extração dos dados específicos de cada edital
            for edital in dados:
                edital_info = {
                    "ID": edital.get("id", "N/A"),
                    "Número": edital.get("numero", "N/A"),
                    "Ano": edital.get("ano", "N/A"),
                    "Número Sequencial": edital.get("numero_sequencial", "N/A"),
                    "Órgão": edital.get("orgao_nome", "N/A"),
                    "Unidade Compradora": edital.get("unidade_nome", "N/A"),
                    "Município": edital.get("municipio_nome", "N/A"),
                    "UF": edital.get("uf", "N/A"),
                    "Modalidade da Contratação": edital.get("modalidade_licitacao_nome", "N/A"),
                    "Amparo Legal": edital.get("amparo_legal", "N/A"),
                    "Tipo": edital.get("tipo_nome", "N/A"),
                    "Modo de Disputa": edital.get("modo_disputa", "N/A"),
                    "Registro de Preço": edital.get("registro_preco", "N/A"),
                    "Data Divulgação PNCP": edital.get("data_publicacao_pncp", "N/A"),
                    "Situação": edital.get("situacao_nome", "N/A"),
                    "Data Início Propostas": edital.get("data_inicio_vigencia", "N/A"),
                    "Data Fim Propostas": edital.get("data_fim_vigencia", "N/A"),
                    "ID Contratação PNCP": edital.get("numero_controle_pncp", "N/A"),
                    "Fonte": "PNCP",
                    "Objeto": edital.get("description", "N/A"),
                    "Informação Complementar": edital.get("informacao_complementar", "N/A"),
                    "URL": f"https://pncp.gov.br{edital.get('item_url', '')}"
                }
                todos_editais.append(edital_info)

            print(f"Editais encontrados na página {pagina}: {len(dados)}")
            pagina += 1  
        else:
            print(f"Erro ao buscar editais: {resposta.status_code} - {resposta.text}")
            break

    print(f"Total de editais encontrados: {len(todos_editais)}")
    return todos_editais

def salvar_em_excel(editais, nome_arquivo="editais.xlsx"):
    """Salva a lista de editais em um arquivo Excel, tratando as datas."""
    if not editais:
        print("Nenhum edital para salvar.")
        return
    
    # Convertendo para um DataFrame do pandas
    df = pd.DataFrame(editais)

    # Tratamento das colunas de data (removendo a parte de horas)
    colunas_data = ["Data Divulgação PNCP", "Data Início Propostas", "Data Fim Propostas"]
    for coluna in colunas_data:
        if coluna in df.columns:
            df[coluna] = df[coluna].astype(str).str.split("T").str[0]  # Mantém apenas a parte da data

    # Salvando no arquivo Excel na raiz do projeto
    df.to_excel(nome_arquivo, index=False)
    print(f"Arquivo salvo com sucesso: {nome_arquivo}")

# Executa a busca
editais = buscar_editais()

# Salva no Excel
salvar_em_excel(editais)
