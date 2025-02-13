**Coleta de Editais do Portal Nacional de Contratações Públicas**

**Descrição**

Este projeto tem como objetivo buscar e coletar automaticamente os editais de licitação publicados no Portal Nacional de Contratações Públicas (PNCP), especificamente para editais publicados dentro dos últimos 15 dias (D-15). O script coleta as informações dos editais e seus itens associados e os salva em uma planilha Excel, sem duplicação de dados, para análise posterior em BI ou outras ferramentas de processamento de dados.

**Requisitos**

° Python 3.x: A versão recomendada para executar este script é Python 3.7 ou superior.

° Bibliotecas Python:
    
    requests: Para realizar as requisições HTTP à API do PNCP.
    
    datetime: Para manipulação de datas.
    
    pandas: Para salvar os dados coletados em formato Excel.
    
    os: Para verificar a existência do arquivo Excel.
    
    openpyxl: Para garantir que o pandas consiga salvar o arquivo Excel corretamente.
    
**Instalação das Bibliotecas**
    
Para instalar as bibliotecas necessárias, execute o seguinte comando:

    pip install requests pandas openpyxl

**Estrutura do Projeto**

O script realiza os seguintes passos:

1. Busca de Editais:

   Faz uma requisição à API do PNCP para obter todos os editais publicados nos últimos 15 dias.

2. Coleta de Detalhes dos Editais:

   Para cada edital encontrado, faz uma nova requisição para obter todos os detalhes desse edital, incluindo os itens associados.

3. Armazenamento em Excel:

   Cria um arquivo Excel, onde cada edital é armazenado em uma linha principal.

   Para cada item dentro de um edital, é criada uma linha subsequente associada ao edital correspondente.

5. Evitar Duplicação:

   O script verifica se o edital já foi processado anteriormente e evita que dados duplicados sejam armazenados na planilha.

**Estrutura da Planilha**

A planilha Excel gerada terá a seguinte estrutura:

**Colunas:**

1. Edital ID: Identificador único do edital.
2. Título: Título do edital.
3. Órgão: Órgão responsável pela publicação do edital.
4. Modalidade: Modalidade da licitação (ex: Concorrência, Pregão, etc.).
5. Data de Publicação: Data em que o edital foi publicado.
6. Status: Status do edital (ex: Aberto, Fechado).
7. Descrição: Descrição do edital.
8. Processo: Número do processo relacionado ao edital.
9. Link: Link para acessar o edital completo.
10. Data Limite: Data limite para a participação na licitação.
11. Item Descrição: Descrição de cada item listado no edital.
12. Quantidade: Quantidade de unidades para o item.
13. Valor Estimado: Valor estimado para o item.

**Fluxo do Script**
1. Busca de Editais: O script faz uma requisição à API do PNCP para buscar os editais publicados nos últimos 15 dias, filtrando pelas datas de publicação. A URL da API usada é:

    https://pncp.gov.br/api/consulta/editais?dataPublicacaoInicio={data_inicio}&dataPublicacaoFim={data_fim}

2. Busca de Itens de Cada Edital: Para cada edital encontrado, o script faz uma requisição adicional para obter os detalhes do edital, incluindo os itens. A URL da API usada é:

    https://pncp.gov.br/api/consulta/editais/{edital_id}

3. Armazenamento de Dados: O script armazena os dados dos editais e seus itens em um arquivo Excel. Para evitar duplicação de dados, ele verifica se o Edital ID já existe no arquivo antes de adicionar novos dados.

4. Atualização Diária: O script pode ser configurado para rodar automaticamente todos os dias, garantindo que os dados no arquivo Excel sejam atualizados com os editais mais recentes e novos itens.


**Conclusão**

Esse projeto permite que você colete editais e itens do PNCP de forma automatizada e os armazene de maneira organizada em uma planilha Excel, facilitando a análise de dados. Ele pode ser executado diariamente para garantir que os dados estejam sempre atualizados. Se precisar de mais ajustes ou tiver outras dúvidas, estou à disposição!
