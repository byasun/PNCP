import os
import pandas as pd
from src.Salvar_Dados import salvar_editais_com_itens, salvar_atas_e_contratos

def testar_salvar_editais_com_itens():
    """Testa se os editais e itens são salvos corretamente em um arquivo Excel."""
    arquivo_teste = "test_editais_itens.xlsx"

    # Criando dados fictícios
    editais = [
        {"ID Edital": "123", "Título": "Edital de Teste 1", "Órgão": "Órgão X", "Data Publicação": "2025-02-25"},
        {"ID Edital": "456", "Título": "Edital de Teste 2", "Órgão": "Órgão Y", "Data Publicação": "2025-02-26"}
    ]

    itens = [
        {"ID Edital": "123", "Número Item": "1", "Descrição Item": "Item de teste A"},
        {"ID Edital": "123", "Número Item": "2", "Descrição Item": "Item de teste B"},
        {"ID Edital": "456", "Número Item": "1", "Descrição Item": "Item de teste C"}
    ]

    # Salvar no arquivo
    salvar_editais_com_itens(editais, itens, nome_arquivo=arquivo_teste)

    # Verifica se o arquivo foi criado
    assert os.path.exists(arquivo_teste), "Erro: O arquivo Excel não foi criado."

    # Verifica se as abas "Editais" e "Itens" existem no arquivo
    with pd.ExcelFile(arquivo_teste) as xls:
        assert "Editais" in xls.sheet_names, "Erro: Aba 'Editais' não encontrada no Excel."
        assert "Itens" in xls.sheet_names, "Erro: Aba 'Itens' não encontrada no Excel."

    print("Teste de salvar editais e itens PASSED.")

    # Remove o arquivo após o teste para evitar lixo no projeto
    os.remove(arquivo_teste)

def testar_salvar_atas_e_contratos():
    """Testa se as atas e contratos são salvos corretamente em um arquivo Excel."""
    arquivo_teste = "test_atas_contratos.xlsx"

    # Criando dados fictícios
    atas = [
        {"ID Ata": "001", "Descrição": "Ata de Registro 1"},
        {"ID Ata": "002", "Descrição": "Ata de Registro 2"}
    ]

    contratos = [
        {"ID Contrato": "A1", "Descrição": "Contrato de Prestação de Serviço"},
        {"ID Contrato": "A2", "Descrição": "Contrato de Fornecimento"}
    ]

    # Salvar no arquivo
    salvar_atas_e_contratos(atas, contratos, nome_arquivo=arquivo_teste)

    # Verifica se o arquivo foi criado
    assert os.path.exists(arquivo_teste), "Erro: O arquivo Excel não foi criado."

    # Verifica se as abas "Atas" e "Contratos" existem no arquivo
    with pd.ExcelFile(arquivo_teste) as xls:
        assert "Atas" in xls.sheet_names, "Erro: Aba 'Atas' não encontrada no Excel."
        assert "Contratos" in xls.sheet_names, "Erro: Aba 'Contratos' não encontrada no Excel."

    print("Teste de salvar atas e contratos PASSED.")

    # Remove o arquivo após o teste
    os.remove(arquivo_teste)

if __name__ == "__main__":
    testar_salvar_editais_com_itens()
    testar_salvar_atas_e_contratos()
