import aiohttp
import asyncio
import time
from src.config import BASE_URL, HEADERS
from src.utils import Formatar_Data, Remover_Caracteres_Invalidos
from src.Busca_Itens import buscar_itens_de_edital

async def buscar_editais():
    """Busca os editais e já dispara a busca dos itens em paralelo enquanto busca outros editais."""
    todos_editais = []
    pagina = 1
    tam_pagina = 100  # Reduzido para diminuir chances de erro 429
    semaforo = asyncio.Semaphore(45)  # Controla quantas requisições podem ocorrer simultaneamente

    paginas_por_tempo = 5  # Número de páginas antes de exibir tempo decorrido
    tempo_inicio = time.time()  # Inicia o contador

    async with aiohttp.ClientSession() as session:
        while True:

            if (pagina - 1) % paginas_por_tempo == 0 and pagina > 1:
                tempo_decorrido = time.time() - tempo_inicio
                minutos, segundos = divmod(int(tempo_decorrido), 60)
                print(f"Concluída a busca de itens para as Páginas {pagina - paginas_por_tempo} a {pagina - 1} de editais em {minutos:02d}:{segundos:02d}.")
                tempo_inicio = time.time()  # Reinicia o contador para as próximas 5 páginas

            params = {
                "tipos_documento": "edital",
                "ordenacao": "-data",
                "pagina": pagina,
                "tam_pagina": tam_pagina,
                "status": "recebendo_proposta"
            }

            print(f"Buscando editais - Página {pagina}...")
            async with session.get(BASE_URL, headers=HEADERS, params=params) as resposta:
                if resposta.status == 200:
                    dados = await resposta.json()
                    items = dados.get("items", [])
                    if not items:
                        break

                    # Criar lista de tarefas para buscar itens enquanto busca os editais
                    tarefas_itens = []
                    for edital in items:
                        edital_info = {chave: Remover_Caracteres_Invalidos(edital.get(chave, "N/A")) for chave in edital}
                        edital_info["data_publicacao_pncp"] = Formatar_Data(edital_info.get("data_publicacao_pncp"))

                        # Inicia a busca de itens imediatamente após encontrar o edital
                        tarefas_itens.append(buscar_itens_de_edital(session, edital_info, semaforo))

                        # Adiciona o edital à lista de editais a serem retornados
                        todos_editais.append(edital_info)

                    # Aguarda todas as buscas de itens para os editais de forma assíncrona
                    await asyncio.gather(*tarefas_itens)

                    print(f"Concluída a busca de itens para a Página {pagina} de editais.")

                    # Pequena pausa para evitar sobrecarga na API
                    await asyncio.sleep(0.5)

                    pagina += 1

                elif resposta.status == 429:
                    print("API limitando requisições. Aguardando antes de tentar novamente...")
                    await asyncio.sleep(10)  # Aguarda 10 segundos antes de tentar novamente
                else:
                    print(f"Erro ao buscar editais: {resposta.status} - {resposta.text}")
                    break

    return todos_editais