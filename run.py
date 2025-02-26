import asyncio
from src.Busca_Editais import buscar_editais
from src.Busca_Atas import buscar_atas_em_lote
from src.Busca_Contratos import buscar_contratos_em_lote
from src.Salvar_Dados import salvar_editais_com_itens, salvar_atas_e_contratos

async def main():
    # Busca os editais e já busca os itens simultaneamente
    editais = await buscar_editais()

    # Extraindo os itens corretamente
    itens = [item for edital in editais for item in edital.get("itens", [])]

    # Salva os dados de editais com itens em um arquivo Excel
    salvar_editais_com_itens(editais, itens)

    # Busca as atas e contratos
    atas, contratos = await asyncio.gather(
        buscar_atas_em_lote(),
        buscar_contratos_em_lote()
    )

    # Salva as atas e contratos em outro arquivo Excel
    await salvar_atas_e_contratos(atas, contratos)

if __name__ == "__main__":
    asyncio.run(main())
