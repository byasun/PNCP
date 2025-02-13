import requests
import datetime
import pandas as pd
import os

# URL base da API do PNCP
BASE_URL = "https://pncp.gov.br/api/consulta"

# Calcula a data de D-15
hoje = datetime.date.today()
data_inicio = hoje - datetime.timedelta(days=15)
data_fim = hoje

# Converte as datas para o formato esperado (AAAA-MM-DD)
data_inicio_str = data_inicio.strftime("%Y-%m-%d")
data_fim_str = data_fim.strftime("%Y-%m-%d")

# Nome do arquivo Excel
NOME_ARQUIVO = "editais_com_itens.xlsx"

def buscar_editais():
    """Busca todos os editais publicados nos últimos 15 dias."""
    url = f"{BASE_URL}/editais?dataPublicacaoInicio={data_inicio_str}&dataPublicacaoFim={data_fim_str}"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        return resposta.json()
    else:
        print(f"Erro ao buscar editais: {resposta.status_code}")
        return []

def buscar_detalhes_edital(edital_id):
    """Busca detalhes completos de um edital específico pelo ID."""
    url = f"{BASE_URL}/editais/{edital_id}"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        return resposta.json()
    else:
        print(f"Erro ao buscar detalhes do edital {edital_id}: {resposta.status_code}")
        return None

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
    """Busca os editais e automaticamente busca os detalhes completos de cada um, sem duplicar."""
    # Carrega dados existentes
    dados_existentes = carregar_dados_existentes()
    ids_existentes = dados_existentes["Edital ID"].tolist() if not dados_existentes.empty else []

    editais = buscar_editais()
    lista_dados = []
    
    for edital in editais:
        edital_id = edital.get("id")
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
            
            # Coleta e adiciona os itens do edital como linhas subsequentes
            itens = detalhes.get("itens", [])
            for item in itens:
                dados_item = {
                    "Edital ID": edital_id,
                    "Título": "",  # Deixamos em branco, pois a linha do edital já contém esse dado
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
