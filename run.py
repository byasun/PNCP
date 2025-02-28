import asyncio
from src.Busca_Editais import buscar_editais, buscar_itens_para_todos_editais
from src.Busca_Atas import buscar_atas_em_lote
from src.Busca_Contratos import buscar_contratos_em_lote
from src.Salvar_Dados import salvar_dados_editais_itens, salvar_atas, salvar_contratos

async def main():
    # Busca os editais
    editais = await buscar_editais()

    if not editais:
        print("\nNenhum edital encontrado.")
        return

    print(f"\n{len(editais)} editais coletados.")
    print("\nExemplo de edital coletado:")
    print(editais[0])  # Apenas para conferência

    # Busca os itens separadamente
    itens = await buscar_itens_para_todos_editais(editais)

    if not itens:
        print("\nNenhum item encontrado.")
    else:
        print(f"\n{len(itens)} itens coletados.")
       # print(itens[0])  # Apenas para conferência

    # Salva os editais e itens
    salvar_dados_editais_itens(editais, itens)

    # Busca atas e contratos
    atas, contratos = await asyncio.gather(
        buscar_atas_em_lote(),
        buscar_contratos_em_lote()
    )

    if atas:
        print(f"\n{len(atas)} atas coletadas.")
    if contratos:
        print(f"\n{len(contratos)} contratos coletados.")

    # Salva atas e contratos
    salvar_atas(atas)
    salvar_contratos(contratos)

    print("\nProcessamento concluído com sucesso.")

if __name__ == "__main__":
    asyncio.run(main())
