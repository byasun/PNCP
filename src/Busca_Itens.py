import aiohttp
import asyncio
import random
from src.config import BASE_URL_ITENS, HEADERS

async def buscar_itens_de_edital(session, edital, semaforo):
    """Busca os itens de um edital específico com paginação, 5 itens por página."""
    cnpj = edital.get("orgao_cnpj", "").strip()
    ano = edital.get("ano", "").strip()
    num_seq = edital.get("numero_sequencial", "").strip()
    
    if not cnpj or not ano or not num_seq:
        return []

    url_base = f"{BASE_URL_ITENS}/{cnpj}/compras/{ano}/{num_seq}/itens"
    tam_pagina = 5
    pagina = 1
    itens_lista = []

    try:
        while True:
            await asyncio.sleep(random.uniform(1, 3))  # Delay aleatório para evitar bloqueios
            url = f"{url_base}?pagina={pagina}&tamanhoPagina={tam_pagina}"
            tentativas = 0

            while tentativas < 5:
                try:
                    async with semaforo, session.get(url, headers=HEADERS) as resposta:
                        if resposta.status == 200:
                            dados = await resposta.json()
                            if not dados or len(dados) < tam_pagina:  # Menos de 5 itens ou resposta vazia
                                return itens_lista

                            for item in dados:
                                itens_lista.append({
                                    "ID Edital": edital.get("id", "N/A"),
                                    "Número Item": item.get("numeroItem", "N/A"),
                                    "Descrição Item": item.get("descricao", "N/A"),
                                    "Material ou Serviço": item.get("materialOuServicoNome", "N/A"),
                                    "Valor Unitário Estimado": item.get("valorUnitarioEstimado", "N/A"),
                                    "Valor Total": item.get("valorTotal", "N/A"),
                                    "Quantidade": item.get("quantidade", "N/A"),
                                    "Unidade Medida": item.get("unidadeMedida", "N/A"),
                                    "Critério de Julgamento": item.get("criterioJulgamentoNome", "N/A"),
                                    "Situação do Item": item.get("situacaoCompraItemNome", "N/A"),
                                    "Tipo de Benefício": item.get("tipoBeneficioNome", "N/A"),
                                    "Data Inclusão": item.get("dataInclusao", "N/A"),
                                    "Data Atualização": item.get("dataAtualizacao", "N/A")
                                })

                            pagina += 1  # Avançamos para a próxima página
                            break  # Sai do loop de tentativas se deu certo

                        elif resposta.status == 429:
                            tentativas += 1
                            espera = min(2 ** tentativas, 60)
                            print(f"Erro 429 ao buscar página {pagina}. Esperando {espera}s...")
                            await asyncio.sleep(espera)
                        else:
                            print(f"Erro {resposta.status} ao buscar página {pagina}.")
                            return itens_lista

                except Exception as e:
                    print(f"Erro inesperado na página {pagina}: {str(e)}")
                    return itens_lista

    except Exception as e:
        print(f"Erro ao buscar itens para o edital {edital.get('id', 'N/A')}: {str(e)}")

    return itens_lista
