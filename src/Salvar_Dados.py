import pandas as pd
import openpyxl
from datetime import datetime

def salvar_dados_editais_itens(editais, itens):
    # Criação do DataFrame para os Editais com todos os campos
    df_editais = pd.DataFrame(editais)

    # Criação do DataFrame para os Itens
    df_itens = pd.DataFrame(itens)

    # Nome do arquivo com data para evitar sobrescrever
    nome_arquivo = f'dados_editais_itens_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'

    # Escreve os dados dos editais e dos itens no mesmo arquivo Excel
    with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
        df_editais.to_excel(writer, sheet_name='Editais', index=False)
        df_itens.to_excel(writer, sheet_name='Itens', index=False)

# Função para coletar os itens
def buscar_itens_edital(api_response):
    itens = []
    for item in api_response:
        # Criação de um dicionário com os dados do item
        item_data = {
            'numeroItem': item['numeroItem'],
            'descricao': item['descricao'],
            'materialOuServico': item['materialOuServicoNome'],
            'valorUnitarioEstimado': item['valorUnitarioEstimado'],
            'valorTotal': item['valorTotal'],
            'quantidade': item['quantidade'],
            'unidadeMedida': item['unidadeMedida'],
            'dataInclusao': item['dataInclusao'],
            'dataAtualizacao': item['dataAtualizacao']
        }
        itens.append(item_data)
    
    return itens

# Função para processar os editais e salvar as informações completas
def salvar_dados_edital_completo(edital_response):
    editais = []
    
    # Criação de um dicionário com os dados completos do edital
    edital_data = {
        'id': edital_response['id'],
        'titulo': edital_response['title'],
        'descricao': edital_response['description'],
        'item_url': edital_response['item_url'],
        'document_type': edital_response['document_type'],
        'createdAt': edital_response['createdAt'],
        'numero': edital_response['numero'],
        'ano': edital_response['ano'],
        'numero_sequencial': edital_response['numero_sequencial'],
        'numero_controle_pncp': edital_response['numero_controle_pncp'],
        'orgao_id': edital_response['orgao_id'],
        'orgao_cnpj': edital_response['orgao_cnpj'],
        'orgao_nome': edital_response['orgao_nome'],
        'unidade_id': edital_response['unidade_id'],
        'unidade_codigo': edital_response['unidade_codigo'],
        'unidade_nome': edital_response['unidade_nome'],
        'esfera_nome': edital_response['esfera_nome'],
        'poder_nome': edital_response['poder_nome'],
        'municipio_nome': edital_response['municipio_nome'],
        'uf': edital_response['uf'],
        'modalidade_licitacao_nome': edital_response['modalidade_licitacao_nome'],
        'situacao_nome': edital_response['situacao_nome'],
        'data_publicacao_pncp': edital_response['data_publicacao_pncp'],
        'data_atualizacao_pncp': edital_response['data_atualizacao_pncp'],
        'data_inicio_vigencia': edital_response['data_inicio_vigencia'],
        'data_fim_vigencia': edital_response['data_fim_vigencia'],
        'cancelado': edital_response['cancelado'],
        'valor_global': edital_response['valor_global'],
        'tem_resultado': edital_response['tem_resultado'],
        'tipo_nome': edital_response['tipo_nome'],
        'tipo_contrato_nome': edital_response['tipo_contrato_nome']
    }
    
    editais.append(edital_data)
    
    return editais

def salvar_atas(atas):
    """Salva os dados das atas em um arquivo Excel."""
    if not atas:
        print("\nNenhuma ata encontrada para salvar.")
        return

    # Criação do DataFrame para as Atas
    df_atas = pd.DataFrame(atas)

    # Nome do arquivo com data para evitar sobrescrever
    nome_arquivo_atas = f'dados_atas.xlsx'

    # Salva as atas no arquivo Excel
    with pd.ExcelWriter(nome_arquivo_atas, engine='openpyxl') as writer:
        df_atas.to_excel(writer, sheet_name='Atas', index=False)

def salvar_contratos(contratos):
    """Salva os dados dos contratos em um arquivo Excel."""
    if not contratos:
        print("\nNenhum contrato encontrado para salvar.")
        return

    # Criação do DataFrame para os Contratos
    df_contratos = pd.DataFrame(contratos)

    # Nome do arquivo com data para evitar sobrescrever
    nome_arquivo_contratos = f'dados_contratos.xlsx'

    # Salva os contratos no arquivo Excel
    with pd.ExcelWriter(nome_arquivo_contratos, engine='openpyxl') as writer:
        df_contratos.to_excel(writer, sheet_name='Contratos', index=False)