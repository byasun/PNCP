import asyncio
from src.Busca_Editais import buscar_editais_em_lote
from src.Busca_Atas import buscar_atas_em_lote
from src.Busca_Contratos import buscar_contratos_em_lote
from src.Busca_Itens import buscar_itens_de_edital
from src.Salvar_Dados import salvar_editais_com_itens, salvar_atas_e_contratos

if __name__ == "__main__":
    # Busca os editais
    editais = asyncio.run(buscar_editais_em_lote())

    # Agora buscamos os itens para cada edital
    itens = []

    for edital in editais:
        # Chama a função para buscar itens de cada edital individualmente
        itens_de_edital = asyncio.run(buscar_itens_de_edital(edital))
        itens.extend(itens_de_edital)  # Adiciona os itens coletados para o edital ao resultado

    # Salva os dados de editais com itens em um arquivo Excel
    salvar_editais_com_itens(editais, itens)

    # Busca as atas e contratos
    atas = asyncio.run(buscar_atas_em_lote())
    contratos = asyncio.run(buscar_contratos_em_lote())

    # Salva as atas e contratos em outro arquivo Excel
    salvar_atas_e_contratos(atas, contratos)
