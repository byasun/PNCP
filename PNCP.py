import requests
import datetime
import pandas as pd
import os

# URL base da API do PNCP
BASE_URL = "https://pncp.gov.br/pncp-consulta/v1"

# Lista de modalidades corrigida (agora são strings, não números)
MODALIDADES = {
    1: "Leilão - Eletrônico",
    2: "Diálogo Competitivo",
    3: "Concurso",
    4: "Concorrência - Eletrônica",
    5: "Concorrência - Presencial",
    6: "Pregão - Eletrônico",
    7: "Pregão - Presencial",
    8: "Dispensa de Licitação",
    9: "Inexigibilidade",
    10: "Manifestação de Interesse",
    11: "Pré-qualificação",
    12: "Credenciamento",
    13: "Leilão - Presencial"
}

# Calcula a data de D-15
hoje = datetime.date.today()
data_inicio = hoje - datetime.timedelta(days=15)
data_fim = hoje

# Converte as datas para o formato esperado (yyyyMMdd)
data_inicio_str = data_inicio.strftime("%Y%m%d")
data_fim_str = data_fim.strftime("%Y%m%d")

# Nome do arquivo Excel
NOME_ARQUIVO = "editais_com_itens.xlsx"

# Cabeçalhos da requisição
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def buscar_editais_por_modalidade(modalidade_codigo):
    """Busca todas as contratações publicadas nos últimos 15 dias para uma modalidade específica, paginando os resultados."""
    todos_editais = []
    pagina = 1  # Iniciamos na página 1

    while True:
        url = f"{BASE_URL}/contratacoes/publicacao"
        params = {
            "dataInicial": data_inicio_str,  # Agora no formato yyyyMMdd
            "dataFinal": data_fim_str,       # Agora no formato yyyyMMdd
            "codigoModalidadeContratacao": modalidade_codigo,  # Agora utilizando o código da modalidade
            "pagina": pagina
        }
        
        resposta = requests.get(url, headers=HEADERS, params=params)

        if resposta.status_code == 200:
            dados = resposta.json().get("contratacoes", [])
            if not dados:
                break  # Se não houver mais editais, encerramos a paginação
            todos_editais.extend(dados)
            print(f"Editais encontrados para a modalidade {modalidade_codigo}: {len(dados)}")  # Exibe o número de editais encontrados
            pagina += 1  # Passamos para a próxima página
        else:
            print(f"Erro ao buscar editais da modalidade {modalidade_codigo}, página {pagina}: {resposta.status_code} - {resposta.text}")
            break

    print(f"Total de editais encontrados para a modalidade {modalidade_codigo}: {len(todos_editais)}")  # Exibe o total de editais encontrados
    return todos_editais

def buscar_todos_editais():
    """Itera sobre todas as modalidades e busca os editais de cada uma, incluindo paginação."""
    todos_editais = []
    for codigo_modalidade in MODALIDADES:  # Agora itera pelos códigos
        print(f"Buscando editais para a modalidade {MODALIDADES[codigo_modalidade]}")
        editais = buscar_editais_por_modalidade(codigo_modalidade)
        todos_editais.extend(editais)  # Junta todos os editais encontrados
    
    # Exibe o total de editais encontrados em todas as modalidades
    print(f"Total de editais encontrados em todas as modalidades: {len(todos_editais)}")
    return todos_editais

def buscar_detalhes_edital(edital_id):
    """Busca detalhes completos de um edital específico pelo ID."""
    url = f"{BASE_URL}/editais/{edital_id}"
    resposta = requests.get(url, headers=HEADERS)

    if resposta.status_code == 200:
        return resposta.json()
    else:
        print(f"Erro ao buscar detalhes do edital {edital_id}: {resposta.status_code}")
        return None

def buscar_itens_edital(edital_id):
    """Busca os itens de um edital específico pelo ID."""
    url = f"{BASE_URL}/editais/{edital_id}/itens"
    resposta = requests.get(url, headers=HEADERS)

    if resposta.status_code == 200:
        return resposta.json().get("itens", [])  # Ajustar conforme estrutura do retorno
    else:
        print(f"Erro ao buscar itens do edital {edital_id}: {resposta.status_code}")
        return []

def carregar_dados_existentes():
    """Carrega os dados existentes do arquivo Excel, se ele existir."""
    if os.path.exists(NOME_ARQUIVO):
        return pd.read_excel(NOME_ARQUIVO)
    else:
        return pd.DataFrame()  # Retorna um DataFrame vazio se o arquivo não existir

def salvar_em_excel(dados):
    """Salva os dados em um arquivo Excel."""
    df = pd.DataFrame(dados)
    df.to_excel(NOME_ARQUIVO, index=False)
    print(f"Dados salvos em {NOME_ARQUIVO}")

def processar_editais():
    """Busca os editais e automaticamente busca os detalhes e itens de cada um, sem duplicar."""
    # Carrega dados existentes
    dados_existentes = carregar_dados_existentes()
    ids_existentes = dados_existentes["Edital ID"].tolist() if not dados_existentes.empty else []

    editais = buscar_todos_editais()
    lista_dados = []
    
    for edital in editais:
        edital_id = edital.get("identificador" or "id")  # Ajuste conforme necessário
        if not edital_id or edital_id in ids_existentes:
            continue  # Pula se o edital já foi processado
        
        detalhes = buscar_detalhes_edital(edital_id)
        if detalhes:
            # Coletando dados gerais do edital
            dados_edital = {
                "Edital ID": edital_id,
                "Título": detalhes.get("titulo"),
                "Órgão": detalhes.get("orgao"),
                "Modalidade": detalhes.get("modalidade"),
                "Data de Publicação": detalhes.get("dataPublicacao"),
                "Status": detalhes.get("status"),
                "Descrição": detalhes.get("descricao"),
                "Processo": detalhes.get("processo"),
                "Link": detalhes.get("link"),
                "Data Limite": detalhes.get("dataLimite"),
            }
            
            # Adiciona os dados gerais do edital como linha principal
            lista_dados.append(dados_edital)
            
            # Busca os itens do edital e adiciona como linhas subsequentes
            itens = buscar_itens_edital(edital_id)
            for item in itens:
                dados_item = {
                    "Edital ID": edital_id,
                    "Título": "",  # Deixamos em branco para não repetir os dados do edital
                    "Órgão": "",
                    "Modalidade": "",
                    "Data de Publicação": "",
                    "Status": "",
                    "Descrição": "",
                    "Processo": "",
                    "Link": "",
                    "Data Limite": "",
                    "Item Descrição": item.get("descricao", ""),
                    "Quantidade": item.get("quantidade", ""),
                    "Valor Estimado": item.get("valorEstimado", ""),
                }
                lista_dados.append(dados_item)
    
    # Salvar os dados no Excel se houver novos
    if lista_dados:
        if dados_existentes.empty:
            salvar_em_excel(lista_dados)
        else:
            # Adiciona novos dados à planilha existente
            df_existente = pd.DataFrame(dados_existentes)
            df_novo = pd.DataFrame(lista_dados)
            df_final = pd.concat([df_existente, df_novo], ignore_index=True)
            salvar_em_excel(df_final)
    else:
        print("Nenhum dado novo encontrado para salvar.")

# Executa o script
processar_editais()
