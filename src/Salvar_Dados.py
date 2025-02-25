import pandas as pd

def salvar_editais_com_itens(editais, itens, nome_arquivo="editais_com_itens.xlsx"):
    """Salva editais e itens em um arquivo Excel com abas separadas."""
    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        pd.DataFrame(editais).to_excel(writer, sheet_name="Editais", index=False)
        pd.DataFrame(itens).to_excel(writer, sheet_name="Itens", index=False)

    print(f"Arquivo {nome_arquivo} salvo com sucesso!")

def salvar_atas_e_contratos(atas, contratos, nome_arquivo="atas_e_contratos.xlsx"):
    """Salva atas e contratos em um arquivo Excel com abas separadas."""
    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        pd.DataFrame(atas).to_excel(writer, sheet_name="Atas", index=False)
        pd.DataFrame(contratos).to_excel(writer, sheet_name="Contratos", index=False)

    print(f"Arquivo {nome_arquivo} salvo com sucesso!")
